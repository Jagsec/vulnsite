#This file has all the forms related to challenges

from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import SelectField, StringField, IntegerField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length
from wtforms.widgets import TextArea

#This form is used to filter challenges by category in the index file
class FilterForm(FlaskForm):
    category = SelectField(label='Filter by: ', choices=[('all', 'Show all'),
                                                        ('cryptography', 'Crypto'),
                                                        ('steganography', 'Stego'),
                                                        ('web', 'Web Exploitation')])
    submit = SubmitField(label='Filter')

#This form is used to submit flags for each challenge
class FlagForm(FlaskForm):
    flag = StringField(label='Flag: ', validators=[DataRequired()])
    submit = SubmitField(label='Validate')

#This form is used to create new challenges, the file field is optional since not all challenges need
#a file attached to them
class ChallengeForm(FlaskForm):
    name = StringField(label='Name: ', validators=[DataRequired(), Length(min=5, max=30)])
    category = SelectField(label='Category: ', choices=[('cryptography', 'Crypto'),
                                                        ('steganography', 'Stego'),
                                                        ('web', 'Web Exploitation')])
    description = StringField(label='Description: ', validators=[DataRequired(), Length(min=10, max=200)], widget=TextArea())
    score = IntegerField(label='Score: ', validators=[DataRequired()])
    flag = StringField(label='Flag: ', validators=[DataRequired(), Length(min=10, max=50)])
    file = FileField(label='Attached File: ')
    submit = SubmitField(label='Create')
    
#This form is used to edit existing challenges, it inherits from the challenge creation form
#but adds the delete file field and changes the submit label
class EditForm(ChallengeForm):
    delete_file = BooleanField(label='Delete attached file?')
    submit = SubmitField(label='Edit')