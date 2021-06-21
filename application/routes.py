from flask import redirect, request, url_for
from application import app, db

@app.route('/')
@app.route('/home')
def home():
    return "This is the home page"

@app.route('/selectuser/<user_id>')
def selectuser(user_id = user_id):
    return f"You are now using user {user_id}"

@app.route('/newuser')
def newuser():
    return "Create a new user"

@app.route('/deleteuser/<integer: user_id')
def deluser():
    return f"Deleted user {user_id}"

@app.route('/userdetails/<integer: user_id')
def userdetails(user_id = user_id):
    return "Change user Details"
@app.route('/shiplist/<integer:user_id>')
def shiplist(user_id = user_id):
    return f"this is the ship list for the player with id {user_id}"

@app.route('/ship/<integer:ship_id>')
def ship(ship_id = ship_id):
    return f"This is the ship with id {ship_id}"

@app.route('/newship')
def newship():
    return "You have created a new ship!"

@app.route('/sail/<integer:ship_id>/<integer:route_id>')
def sail(ship_id = ship_id, route_id = route_id):
    return f"Ship {ship_id} is now sailing on route {route_id}"

@app.route('/shipdetails/<integer:ship_id>')
def shipdetails(ship_id=ship_id):
    return f"Here you will be able to change the ship details."

@app.route('/admin')
def admin():
    return "This route will have the options reserved for admin"

@app.route('/makeadmin/<integer: user_id>')
def makeadmin(user_id = user_id):
    return f"User {user_id} is now an admin"

@app.route('/newcity')
def newcity():
    return "You have made a new city"

@app.route('/newroute')
def newroute():
    return "You have made a new route"
