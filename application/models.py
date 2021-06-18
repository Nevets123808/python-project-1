
from application import db

class Users(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username= db.Column(db.String(50), nullable = False)
    email= db.Column(db.String(50), nullable = False)
    admin =db.Column(db.Boolean, default = False)

