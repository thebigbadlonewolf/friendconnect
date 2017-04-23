from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Length

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)
    
class SignupForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('confirm', 'Passwords must match')])
    confirm = PasswordField('Repeat Password')
    
class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    bio = TextAreaField('bio', validators=[Length(min=0, max=140)])
    