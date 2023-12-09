"""Defines the forms used in the application"""
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Email, ValidationError, Optional
from flaskapp.models import User, Book
from flaskapp import bcrypt

class RegistrationForm(FlaskForm):
    """Defines the fields of the registration form"""
    usertype = SelectField('Register As', choices=[('writer', 'Writer'), ('client', 'Client')], validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    address = StringField('Address', validators=[DataRequired()])
    phone = StringField('Phone', validators=[Optional()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=20)])
    submit = SubmitField('Sign up')

    def validate_username(self, username):
        """Checks if the username is not already taken by another user"""
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken, please choose a different one')

    def validate_email(self, email):
        """Checks if the email is already taken by another user"""
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken, please choose a different one')

class LoginForm(FlaskForm):
    """Defines the fields of the login form"""
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    """Defines the fields for updating the account credentials"""
    email = StringField('Email', validators=[DataRequired(), Email()])
    address = StringField('Address', validators=[DataRequired()])
    phone = StringField('Phone', validators=[Optional()])
    old_password = PasswordField('Old Password', )
    new_password = PasswordField('New Password', validators=[Length(min=8, max=20)])
    submit = SubmitField('Update')

    def validate_email(self, email):
        """Checks if the email is already taken by another user"""
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken, please choose a different one')
            

    def validate_old_password(self, old_password):
        """Checks if the old password is valide"""
        if self.new_password.data:
            if not bcrypt.check_password_hash(current_user.password, old_password.data):
                raise ValidationError('Incorrect old password. Please try again.')
        
    def validate_new_password(self, new_password):
        """Checks if the new password is different from the old one"""
        if new_password.data:
            if  self.old_password.data == new_password.data:
                raise ValidationError("You can't use your old password. Please try again.")


        

class AddBookForm(FlaskForm):
    """Defines the fields for uploading a new book form"""
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

    """
    def validate_title(self, title):
        book = Book.query.filter_by(title=title.data).first()
        if Book:
            raise ValidationError('That title is taken, please choose a different one')"""
        

class UpdateBookForm(FlaskForm):
    """Defines the fields for updating an existing book form"""
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
    cover = FileField('Upload cover file', validators=[FileAllowed(['jpg', 'png'])])
    manuscript = FileField('Upload manuscript file', validators=[FileAllowed(['pdf'])])
    price= StringField('Price', validators=[DataRequired()])
    submit = SubmitField('Update')

"""
    def validate_title(self, title):
        book = Book.query.filter_by(title=title.data).first()
        if Book:
            raise ValidationError('That title is taken, please choose a different one')
            """


class FindBook(FlaskForm):
    """Defines the form to search for a book"""
    title = StringField('Title')
    genre = SelectField('Genre', choices=[('', ''),
                                          ('Classics', 'Classics'),
                                          ('Detective and mystery', 'Detective and mystery'),
                                          ('Fantasy', 'Fantasy'),
                                          ('Biographies', 'Biographies'),
                                          ('Horror', 'Horror'),
                                          ('Romance', 'Romance'),
                                          ('Sci-Fi', 'Sci-Fi'),
                                          ('Poetry', 'Poetry')])
    author = StringField('Author')
    submit = SubmitField('Find a Book')