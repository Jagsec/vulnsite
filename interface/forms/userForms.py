#This file has all the forms related to the users.

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length
from wtforms.widgets import TextArea
from interface.models.userModel import Users

#This form is used for logging in users
class LoginForm(FlaskForm):
    username = StringField(label='Username', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    submit = SubmitField(label='Login')

#This form is used to register users
class RegisterForm(FlaskForm):
    #This custom validation is used to prevent usernames from being repeated
    def validate_username(self, username_to_check):
        user = Users.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('This username is not available')

    username = StringField(label='Username', validators=[Length(min=2, max=30), DataRequired()])
    password = PasswordField(label='Password', validators=[Length(min=8), DataRequired()])
    password_confirm = PasswordField(label='Confirm password', validators=[DataRequired()])
    submit = SubmitField(label='Register')

#This form is used for editing an existing user info which is displayed on their profile
class EditForm(FlaskForm):
    profile_desc = StringField(label='Description: ', validators=[DataRequired(), Length(min=10, max=200)], widget=TextArea())
    profile_pic = FileField(label='Profile Picture', validators=[FileAllowed(['jpg', 'png'], 'Only jpg and png formats')])
    delete_pic = BooleanField(label='Delete current profile picture?')
    submit = SubmitField(label='Edit')