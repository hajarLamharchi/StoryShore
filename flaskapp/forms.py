from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Email, ValidationError, Optional
from flaskapp.models import User, Book
from flaskapp import bcrypt


class RegistrationForm(FlaskForm):
    usertype = SelectField('Register As', choices=[('writer', 'Writer'), ('client', 'Client')], validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    address = StringField('Address', validators=[DataRequired()])
    phone = StringField('Phone', validators=[Optional()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken, please choose a different one')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken, please choose a different one')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    address = StringField('Address', validators=[DataRequired()])
    phone = StringField('Phone', validators=[Optional()])
    old_password = PasswordField('Old Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired()])
    submit = SubmitField('Update')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken, please choose a different one')
            

    def validate_old_password(self, old_password):
        if not bcrypt.check_password_hash(current_user.password, old_password.data):
            raise ValidationError('Incorrect old password. Please try again.')
        

class AddBookForm(FlaskForm):
    title = StringField('Book Title', validators=[DataRequired()])
    subtitle = StringField('Book Subitle', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    genre = SelectField('Genre', choices=[('Classics', 'Classics'),
                                          ('Detective and mystery', 'Detective and mystery'),
                                          ('Fantasy', 'Fantasy'),
                                          ('Biographies', 'Biographies'),
                                          ('Horror', 'Horror'),
                                          ('Romance', 'Romance'),
                                          ('Sci-Fi', 'Sci-Fi'),
                                          ('Poetry', 'Poetry')], validators=[DataRequired()])
    cover = FileField('Upload cover file', validators=[FileRequired(), FileAllowed(['jpg', 'png'])])
    manuscript = FileField('Upload manuscript file', validators=[FileRequired(), FileAllowed(['pdf'])])
    price= StringField('Price', validators=[DataRequired()])
    submit = SubmitField('Publish')

    def validate_title(self, title):
        book = Book.query.filter_by(title=title.data).first()
        if Book:
            raise ValidationError('That title is taken, please choose a different one')
        

class UpdateBookForm(FlaskForm):
    title = StringField('Book Title', validators=[DataRequired()])
    subtitle = StringField('Book Subitle', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    genre = SelectField('Genre', choices=[('Classics', 'Classics'),
                                          ('Detective and mystery', 'Detective and mystery'),
                                          ('Fantasy', 'Fantasy'),
                                          ('Biographies', 'Biographies'),
                                          ('Horror', 'Horror'),
                                          ('Romance', 'Romance'),
                                          ('Sci-Fi', 'Sci-Fi'),
                                          ('Poetry', 'Poetry')], validators=[DataRequired()])
    cover = FileField('Upload cover file', validators=[FileRequired(), FileAllowed(['jpg', 'png'])])
    manuscript = FileField('Upload manuscript file', validators=[FileRequired(), FileAllowed(['pdf'])])
    price= StringField('Price', validators=[DataRequired()])
    submit = SubmitField('Update')

    def validate_title(self, title):
        book = Book.query.filter_by(title=title.data).first()
        if Book:
            raise ValidationError('That title is taken, please choose a different one')