from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import data_required

class NewUserForm(FlaskForm):
    name = StringField("Username: ", validators=[data_required()])
    email = StringField("Email address: ", validators=[data_required()])
    submit = SubmitField("Create New User")

class UpdateUserForm(FlaskForm):
    name = StringField("Username: ")
    email = StringField("Email address: ")
    submit = SubmitField("Update Details")

class NewShipForm(FlaskForm):
    name = StringField("Name: ", validators=[data_required()])
    type = SelectField("Ship Type: ", choices = ['Fast', 'Medium', 'Slow'])
    submit = SubmitField("Buy Ship")

class UpdateShipForm(FlaskForm):
    name = StringField("name: ")
    submit = SubmitField("Rename Ship")
