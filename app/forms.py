# app/forms.py
# code used from microblog [Miguel Grinberg]
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField, FileField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length
from flask_wtf.file import FileAllowed
from app.models import User
import sqlalchemy as sa
from app import db

# code by marcel based on microblog [Miguel Grinberg]
class RegistrationForm(FlaskForm):
    # Registration form fields
    username = StringField('Username')
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

# code by marcel based on microblog [Miguel Grinberg]
class LoginForm(FlaskForm):
    # Login form fields
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

# code by marcel based on microblog [Miguel Grinberg]
class EditProfileForm(FlaskForm):
    # Profile editing form fields
    username = StringField('Username')
    first_name = StringField('First Name')
    last_name = StringField('Last Name',)
    street = StringField('Street',)
    city = StringField('City',)
    postal_code = StringField('Postal Code',)
    country = StringField('Country',)
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password')
    password2 = PasswordField('Repeat Password', validators=[EqualTo('password')])
    submit = SubmitField('Update Profile')

    def __init__(self, original_email, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_email = original_email

    def validate_email(self, email):
        if email.data != self.original_email:
            user = db.session.scalar(sa.select(User).where(
                User.email == self.email.data))
            if user is not None:
                raise ValidationError('This E-Mail is already in use, please use a different E-Mail.')
            
# code by marcel based on microblog [Miguel Grinberg]
class RecipeForm(FlaskForm):
    # Recipe Form fields
    title = StringField('Title', validators=[DataRequired(), Length(min=1, max=140)])
    image = FileField('Recipe Image', validators=[FileAllowed(['jpg', 'png'], 'Images only!')])
    ingredients = TextAreaField('Ingredients', validators=[DataRequired()])
    instructions = TextAreaField('Instructions', validators=[DataRequired()])
    submit = SubmitField('Post Recipe')


class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')


class PostForm(FlaskForm):
    post = TextAreaField('Say something', validators=[DataRequired()])
    submit = SubmitField('Submit')