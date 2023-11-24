from flask import render_template, url_for, flash, redirect
from flaskapp.models import User, Book
from flaskapp.forms import RegistrationForm, LoginForm
from flaskapp import app, db, bcrypt
from flask_login import login_user, current_user


@app.route('/', strict_slashes=False)
@app.route('/home', strict_slashes=False)
def home():
    return render_template('home_page.html')


@app.route('/login', methods=['GET', 'POST'], strict_slashes=False)
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
   
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=True)
            flash('Login successful', 'success')
            print('login successful')
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessful, please check email and password')
            print('login unsuccessful')
    return render_template('login_page.html', form=form)


@app.route('/register', methods=['GET', 'POST'], strict_slashes=False)
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                email=form.email.data,
                phone=form.phone.data,
                address=form.address.data,
                password=hashed_password,
                usertype=form.usertype.data)
        db.session.add(user)
        db.session.commit()

        flash('Your account has been created! You are able to log in now!', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)


@app.route('/books', strict_slashes=False)
def books():
    return render_template('shop.html')
