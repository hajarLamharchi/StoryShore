from flask import render_template, url_for, flash, redirect, request
from flaskapp.models import User, Book
from flaskapp.forms import RegistrationForm, LoginForm, UpdateAccountForm, AddBookForm
from flaskapp import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required


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
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessful, please check your credentials and try again')
    return render_template('login_page.html', form=form)


@app.route('/logout', strict_slashes=False)
def logout():
    logout_user()
    return redirect(url_for('home'))


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


@app.route('/dashboard', strict_slashes=False)
@login_required
def dashboard():
    
    return render_template('Dashboard.html')


@app.route('/dashboard/<tab_name>')
@login_required
def load_content(tab_name):
    form = UpdateAccountForm()
    form1 = AddBookForm()
    if tab_name == 'my_account':
        form.phone.data = current_user.phone
        form.email.data = current_user.email 
        form.address.data = current_user.address
       # form.new_password.data = current_user.password
        return render_template(f'{tab_name}.html', form=form)
    if tab_name == 'Publish':
        return render_template(f'{tab_name}.html', form=form1)
    content = render_template(f'{tab_name}.html', form=form)
    return content

@app.route('/update_account', methods={'POST'})
@login_required
def update_account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.new_password.data).decode('utf-8')
        current_user.phone = form.phone.data
        current_user.email = form.email.data
        current_user.address = form.address.data
        current_user.password = hashed_password
        db.session.commit()
        flash('Your Account has been updated!', 'success')
        return redirect(url_for('dashboard'))
    content = render_template(f'my_account.html', form=form)
    return content

@app.route('/publish', methods={'POST'})
@login_required
def publish():
    form = AddBookForm()
    if form.validate_on_submit():
        book = Book(title=form.title.data,
                    subtitle=form.subtitle.data,
                    description=form.description.data,
                    genre=form.genre.data,
                    cover=form.cover.data,
                    manuscript=form.manuscript.data,
                    price=form.price.data)
        db.session.add(book)
        db.session.commit()
        flash('Congratulation! your book has been published', 'success')
        return redirect(url_for('dashboard'))
    content = render_template(f'Publish.html', form=form)
    return content
