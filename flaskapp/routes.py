"""Defines all the routes of the application"""
from flask import send_from_directory, render_template, url_for, flash, redirect, request, jsonify
from flaskapp.models import User, Book, Purchase, Cart
from flaskapp.forms import RegistrationForm, LoginForm, UpdateAccountForm, AddBookForm, UpdateBookForm, FindBook
from flaskapp import app, db, bcrypt, mail
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.utils import secure_filename
import os
from flask_mail import Message


@app.route('/', strict_slashes=False)
@app.route('/home', strict_slashes=False)
def home():
    """Defines the home page route"""
    return render_template('home_page.html')

@app.route('/login', methods=['GET', 'POST'], strict_slashes=False)
def login():
    """Defines the login page"""
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
    """Defines the logout route"""
    logout_user()
    return redirect(url_for('home'))

@app.route('/register', methods=['GET', 'POST'], strict_slashes=False)
def register():
    """Defines the registration system"""
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
    """Defines the route where users can discovers all the books"""
    form = FindBook()
    books = Book.query.all()
    return render_template('shop.html', books=books, form=form)

@app.route('/dashboard', strict_slashes=False)
@login_required
def dashboard():
    """Defines the dashboard page for writer"""
    if current_user.usertype == "writer":
        tab_name = 'dash'
    else: 
        tab_name = 'my_account'
    form = None  # Initialize form to None

    if tab_name == 'my_account':
        form = UpdateAccountForm()
        form.phone.data = current_user.phone
        form.email.data = current_user.email 
        form.address.data = current_user.address
    elif tab_name == 'dash':
        Purchases = db.session.query(Purchase).filter(Purchase.user_id == current_user.id)
        total = 0
        for purchase in Purchases:
            total += int(purchase.amount)

    return render_template('Dashboard.html',
                            tab_name=tab_name,
                            form=form,
                            total=total if tab_name == 'dash' else None)

@app.route('/dashboard/<tab_name>', strict_slashes=False)
@login_required
def load_content(tab_name):
    """Defines the different sections of the dashboard"""
    form = None
    books = None
    total = 0

    if tab_name == 'my_account':
        form = UpdateAccountForm()
        form.phone.data = current_user.phone
        form.email.data = current_user.email 
        form.address.data = current_user.address
        return render_template('Dashboard.html', tab_name=tab_name, form=form)
    if current_user.usertype == "writer": 
        if tab_name == 'Publish':
            form = AddBookForm()
        elif tab_name == 'MyBooks':
            books = db.session.query(Book).filter(Book.author_id == current_user.id).all()
            form = UpdateBookForm()
        elif tab_name == 'dash':
            Purchases = db.session.query(Purchase).filter(Purchase.user_id == current_user.id)
            total = 0
            for purchase in Purchases:
                total += int(purchase.amount)
        return render_template('Dashboard.html',
                                tab_name=tab_name,
                                form=form,
                                books=books if tab_name == 'MyBooks' else None,
                                total=total if tab_name == 'dash' else None)
    else:
        flash('Access denied. You do not have permission to access this page', 'Warning')
        return redirect(url_for('load_content', tab_name="my_account"))

@app.route('/update_account', methods={'POST'}, strict_slashes=False)
@login_required
def update_account():
    """Defines the route for updating account credentials"""
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if not form.new_password.data:
            hashed_password = current_user.password
            app.logger.info("not changed")
        else:
            hashed_password = bcrypt.generate_password_hash(form.new_password.data).decode('utf-8')
            app.logger.info("changed")
        current_user.phone = form.phone.data
        current_user.email = form.email.data
        current_user.address = form.address.data
        current_user.password = hashed_password
        db.session.commit()
        app.logger.info(current_user.password)
        flash('Your Account has been updated!', 'success')
        return redirect(url_for('load_content', tab_name="my_account", form=form))
 
    showError(form)
    return redirect(url_for('load_content', tab_name="my_account", form=form))

@app.route('/publish', methods={'POST'}, strict_slashes=False)
@login_required
def publish():
    """Defines the route to publish a new book"""
    form = AddBookForm()
    books = Book.query.all()
    if form.validate_on_submit():
        cover = request.files['cover']
        manuscript = request.files['manuscript']
        if cover and manuscript:
            cover_filename = secure_filename(cover.filename)
            manuscript_filename = secure_filename(manuscript.filename)

            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

            cover.save(os.path.join(app.config['UPLOAD_FOLDER'], cover_filename))
            manuscript.save(os.path.join(app.config['UPLOAD_FOLDER'], manuscript_filename))
            book = Book(title=form.title.data,
                        subtitle=form.subtitle.data,
                        description=form.description.data,
                        genre=form.genre.data,
                        cover=cover_filename,
                        manuscript=manuscript_filename,
                        price=form.price.data,
                        author_id=current_user.id)
            db.session.add(book)
            db.session.commit()
            flash('Congratulation! your book has been published', 'success')
            return redirect(url_for('load_content', tab_name="Publish"))
    showError(form)
    return redirect(url_for('load_content', tab_name="Publish", form=form, books=books))

@app.route('/books/<path:filename>')
def get_image(filename):
    """Returns the path to the book cover"""
    return send_from_directory(os.path.join(os.getcwd(), 'books'), filename)

@app.route('/get_book_data/<int:book_id>')
def get_book_data(book_id):
    """Returns the book information as a json"""
    book = Book.query.get(book_id)
    return jsonify({
        'title': book.title,
        'subtitle': book.subtitle,
        'description': book.description,
        'genre': book.genre,
        'price': book.price,      
    })

@app.route('/updatebook/<int:book_id>', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def updateBook(book_id):
    """Defines the route to update the book information"""
    book = Book.query.filter_by(id=book_id).first()
    form = UpdateBookForm(obj=book)
    if form.validate_on_submit():
        cover = request.files['cover']
        manuscript = request.files['manuscript']
       
        cover_filename = book.cover
        manuscript_filename = book.manuscript
        if cover:
            cover_filename = secure_filename(cover.filename)
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            cover.save(os.path.join(app.config['UPLOAD_FOLDER'], cover_filename))
            
        if manuscript:
            manuscript_filename = secure_filename(manuscript.filename)
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            manuscript.save(os.path.join(app.config['UPLOAD_FOLDER'], manuscript_filename))       
        book.title = form.title.data
        book.subtitle = form.subtitle.data
        book.description = form.description.data
        book.genre = form.genre.data
        book.cover = cover_filename
        book.manuscript = manuscript_filename
        book.price = form.price.data
        db.session.commit()
        flash('Congratulation! your book has been updated', 'success')
        return redirect(url_for('load_content', tab_name="MyBooks"))
    showError(form)
    return redirect(url_for('load_content', tab_name="MyBooks"))

@app.route("/Purchase/<bookId>/<amount>", methods=['POST'], strict_slashes=False)
@login_required
def purchase(bookId, amount):
    """Defines the purchase system"""
    purchase = Purchase(book_id=bookId, user_id=current_user.id, amount=amount)
    book = Book.query.get(bookId)
    upload_link =  book.manuscript 
    send_upload_email(current_user.email, upload_link)
    db.session.add(purchase)
    db.session.commit()
    return ('Status:OK')

@app.route("/cart", strict_slashes=False)
@login_required
def goToCart():
    """Defines the cart route"""
    carts = db.session.query(Cart).filter(Cart.user_id == current_user.id)
    cartInfo = []
    for cart in carts:
        book = Book.query.filter(Book.id == cart.book_id).first()
        author = User.query.filter(User.id == book.author_id).first()
        cartInfo.append({'id': cart.id,
                         'quantity': cart.quantity,
                         'bookId': cart.book_id,
                         'book': book.title,
                         'cover': book.cover,
                         'price': book.price,
                         'Author': author.username})

    return render_template('cart.html', carts=cartInfo)

@app.route("/addToCart/<int:book_id>", methods=['POST'], strict_slashes=False)
@login_required
def addToCart(book_id):
    """Defines the add to cart system"""
    cart = Cart.query.filter(Cart.book_id == book_id).first()
    if not cart: 
        cart = Cart(quantity=1,
                book_id=book_id,
                user_id= current_user.id)
        db.session.add(cart)
    else:
        cart.quantity = 1
    db.session.commit()
    return ('Status:OK')

@app.route("/updateCart/<int:cart_id>/<int:qty>", methods=['POST'], strict_slashes=False)
def updateCart(cart_id, qty):
    """Defines the update cart system"""
    cart = Cart.query.get(cart_id)
    cart.quantity = qty
    app.logger.info(cart.id)
    app.logger.info(qty)
    db.session.commit()
    return ('Status:OK')

@app.route("/removeFromCart/<int:cart_id>", methods=['POST'], strict_slashes=False)
def RemoveFromCart(cart_id):
    """Defines the remove from cart system"""
    cart = Cart.query.get(cart_id)
    db.session.delete(cart)
    db.session.commit()
    return ('Status:OK')


def showError(form):
    """Returns the error message"""
    for field, error_messages in form.errors.items():
        for error_message in error_messages:
            flash(f"{error_message}")


def send_upload_email(email, upload_link):
    """Defines the system for sending upload link to the client email"""
    try:
        msg = Message('Upload your Book', recipients=[email], sender="noreply@storyshore.com")
        path = os.path.join(os.getcwd(), 'books', upload_link)
        with open(path, 'rb') as file:
            msg.attach(upload_link, "application/pdf", file.read())
        msg.body = f'Click the following link to upload your book'
        mail.send(msg)
    except Exception as e:
        app.logger.info(f"Error sending email: {e}")


@app.route('/upload_product', methods=['GET', 'POST'])
@login_required
def upload_product():
    """Defines the route for uploading purchased product"""
    p = Purchase.query.filter_by(user_id=current_user.id).first()
    book = Book.query.get(p.book_id)
    if book:
        upload_link = book.cover
        send_upload_email(current_user.email, upload_link)
        flash('An e-mail has been sent to upload your purchased book')
    return render_template('cart.html')

@app.route('/book/<int:book_id>', methods=['GET', 'POST'])
def getBook(book_id):
    """Defines the route to display book information"""
    book = Book.query.get(book_id)
    author = User.query.get(book.author_id)
    book = {
        'id': book.id,
        'title': book.title,
        'subtitle': book.subtitle,
        'description': book.description,
        'price': book.price,
        'cover': book.cover,
        'author': author.username
    }
    app.logger.info(book)
    return render_template('book_page.html', book=book, author=author)


@app.route('/find_book', methods=['POST', 'GET'])
def find_book():
    """Defines the route for filtering book by title, genre, or author name"""
    form = FindBook()
    results =  db.session.query(Book)
    if form.validate_on_submit():
        title = form.title.data
        genre = form.genre.data
        author = form.author.data
        if title:
            results = results.filter((Book.title.contains(title)))
        if genre:
            results = results.filter((Book.genre.contains(genre)))
        if author:
            results = results.join(User).filter((User.username.contains(author)))
      
        if not results:
            flash("The book you are looking for can't be found")
        return render_template('shop.html', form=form, books=results.all())
    results =  Book.query.all()
    return render_template('shop.html', form=form, books=results)