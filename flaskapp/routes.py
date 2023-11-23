from flask import render_template, url_for, flash, redirect
from flaskapp.models import User, Book
from flaskapp.forms import RegistrationForm, LoginForm
from flaskapp import app

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
