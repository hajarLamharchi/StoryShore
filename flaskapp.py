from flask import Flask, render_template


app = Flask(__name__)


@app.route('/', strict_slashes=False)
@app.route('/home', strict_slashes=False)
def home():
    return render_template('home_page.html')


@app.route('/login', strict_slashes=False)
def login():
    return render_template('login_page.html')


@app.route('/register', strict_slashes=False)
def register():
    return render_template('signup.html')


@app.route('/books', strict_slashes=False)
def books():
    return render_template('shop.html')


if __name__ == '__main__':
    app.run(debug=True)