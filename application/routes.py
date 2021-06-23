from flask import redirect, request, url_for, render_template
from application import app, db
from application.models import Users, Cities, Ships, Routes
from application.forms import NewUserForm

@app.route('/')
@app.route('/home')
def home():
    users = Users.query.all()
    return render_template('home.html', users=users)

@app.route('/selectuser/<int:user_id>')
def selectuser(user_id):
    return f"You are now using user {user_id}"

@app.route('/newuser', methods = ['GET','POST'])
def newuser():
    form = NewUserForm()
    if form.validate_on_submit():
        username = form.name.data
        email =form.email.data
        newuser = Users(username=username,email=email)
        db.session.add(newuser)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('newuser.html', form = form)

@app.route('/deleteuser/<int:user_id>')
def deleteuser(user_id):
    return f"Deleted user {user_id}"

@app.route('/userdetails/<int:user_id>')
def userdetails(user_id):
    return "Change user Details"

@app.route('/shiplist/<int:user_id>')
def shiplist(user_id):
    return f"this is the ship list for the player with id {user_id}"

@app.route('/ship/<int:ship_id>')
def ship(ship_id):
    return f"This is the ship with id {ship_id}"

@app.route('/newship')
def newship():
    return "You have created a new ship!"

@app.route('/sail/<int:ship_id>/<int:route_id>')
def sail(ship_id, route_id):
    return f"Ship {ship_id} is now sailing on route {route_id}"

@app.route('/shipdetails/<int:ship_id>')
def shipdetails(ship_id):
    return f"Here you will be able to change the ship details."

@app.route('/admin')
def admin():
    return "This route will have the options reserved for admin"

@app.route('/makeadmin/<int:user_id>')
def makeadmin(user_id):
    return f"User {user_id} is now an admin"

@app.route('/newcity')
def newcity():
    return "You have made a new city"

@app.route('/newroute')
def newroute():
    return "You have made a new route"
