from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.fields.core import IntegerField
from wtforms.validators import data_required

from application import db
from application.models import Users

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
    city = SelectField("City to build in: ", choices = [])
    submit = SubmitField("Buy Ship")

class UpdateShipForm(FlaskForm):
    name = StringField("name: ")
    submit = SubmitField("Rename Ship")

class MakeAdminForm(FlaskForm):
    #We don't assign any choices, in case the db hasn't been set up
    #We assing the choices before the form is used anyway
    user = SelectField("User: ", choices = [])
    submit = SubmitField("Make Admin")

class NewCityForm(FlaskForm):
    name = StringField("Name: ", validators=[data_required()])
    submit = SubmitField("Found City")

class NewRouteForm(FlaskForm):
    destination = SelectField("Destination: ", choices=[])
    length = IntegerField("Length: ")
    submit = SubmitField("Create Route")

class SailForm(FlaskForm):
    destination = SelectField("Destination: ", choices = [])
    submit = SubmitField("Set Sail!")