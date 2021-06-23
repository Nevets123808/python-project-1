from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

class NewUserForm(FlaskForm):
    name = StringField("Username: ")
    email = StringField("Email address: ")
    submit = SubmitField("Create New User")