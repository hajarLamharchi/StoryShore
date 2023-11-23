from flaskapp import db


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