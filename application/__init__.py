from flask import Flask
from flask-sqlalchemy import SQLAlchemy
from os import getenv
app = Flask(__name__)

app.config['SQL_ALCHEMY_DATABASE_URI'] = getenv("DATABASE_URI")
app.config['SECRET_KEY'] = getenv("SECRET_KEY")

db = SQLALCHEMY(app)

from application import routes
