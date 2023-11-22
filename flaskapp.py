from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm


app = Flask(__name__)
app.config['SECRET_KEY'] = 'e9b92d3e660ad20d'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    address = db.Column(db.String(128))
    password = db.Column(db.String(60), nullable=False)
    user_type = db.Column(db.String(10), nullable=False)
    books = db.relationship('Book', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.user_type}', '{self.username}', '{self.email}')"


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), unique=True, nullable=False)
    subtitle = db.Column(db.String(60), nullable=False)
    description = db.Column(db.String(128), nullable=False)
    genre = db.Column(db.String(128), nullable=False)
    cover = db.Column(db.String(50), nullable=False)
    manuscript = db.Column(db.String(128), nullable=False)
    price= db.Column(db.Integer)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"('{self.title}', '{self.subtitle}', '{self.genre}')"


@app.route('/', strict_slashes=False)
@app.route('/home', strict_slashes=False)
def home():
    return render_template('home_page.html')


@app.route('/login', methods=['Get', 'POST'], strict_slashes=False)
def login():
    form = LoginForm()
    return render_template('login_page.html', form=form)


@app.route('/register', methods=['Get', 'POST'], strict_slashes=False)
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash('Account successfully created for {}'.format(form.username.data), 'success')
        return redirect(url_for('home'))
    return render_template('signup.html', form=form)


@app.route('/books', strict_slashes=False)
def books():
    return render_template('shop.html')


if __name__ == '__main__':
    app.run(debug=True)