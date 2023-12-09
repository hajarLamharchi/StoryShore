"""Defines all the model used in the application"""
from flaskapp import db, login_manager
from flask_login import UserMixin
import json
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    """Defines the user model"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    address = db.Column(db.String(128))
    password = db.Column(db.String(60), nullable=False)
    usertype = db.Column(db.String(10), nullable=False)
    books = db.relationship('Book', backref='author', lazy=True)

    def __repr__(self):
        """Returns a customized representation of a user instance"""
        return f"User('{self.id}','{self.usertype}', '{self.username}', '{self.email}')"


class Book(db.Model):
    """Defines the book model"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), unique=True, nullable=False)
    subtitle = db.Column(db.String(60), nullable=False)
    description = db.Column(db.String(128), nullable=False)
    genre = db.Column(db.String(60), nullable=False)
    cover = db.Column(db.String(128), nullable=False)
    manuscript = db.Column(db.String(128), nullable=False)
    price= db.Column(db.Integer)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    #cover = db.Column(db.LargeBinary)

    def __repr__(self):
        """Returns a customized representation of a book instance"""
        return f"Book('{self.id}','{self.title}', '{self.subtitle}', '{self.genre}')"
    
    def to_dict(self):
        new_dict = self.__dict__.copy()
        new_dict["__class__"] = self.__class__.__name__
        if "_sa_instance_state" in new_dict:
            del new_dict["_sa_instance_state"]
        return new_dict
    

class Purchase(db.Model):
    """Defines the purchase model"""
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Integer, nullable=False)

class Cart(db.Model):
    """Defines the cart model"""
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


