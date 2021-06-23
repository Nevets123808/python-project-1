from flask import redirect, request, url_for, render_template
from application import app, db
from application.models import Users, Cities, Ships, Routes
from application.forms import NewUserForm, UpdateUserForm, NewShipForm

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
    user_to_delete = Users.query.get(user_id)
    db.session.delete(user_to_delete)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/userdetails/<int:user_id>', methods =['GET','POST'])
def userdetails(user_id):
    form = UpdateUserForm()
    user = Users.query.get(user_id)
    if form.validate_on_submit():
        username = form.name.data
        email = form.email.data
        #If there is nothing in the form field, don't update
        if username:
            user.username = username
        if email:
            user.email=email
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('updateuser.html', form = form)

@app.route('/<int:user_id>/shiplist')
def shiplist(user_id):
    user = Users.query.get(user_id)
    ships = Ships.query.filter_by(owner_id = user_id).all()
    return render_template('shiplist.html', user = user, ships = ships)

@app.route('/<int:user_id>/ship/<int:ship_id>')
def ship(user_id, ship_id):
    return f"This is the ship with id {ship_id}"

@app.route('/<int:user_id>/newship', methods = ['GET','POST'])
def newship(user_id):
    user = Users.query.get(user_id)
    form = NewShipForm()
    if form.validate_on_submit():
        shipname = form.name.data
        type = form.type.data
        #Might seem a strange order, but forces "Medium" as default
        if type == 'Fast':
            speed = 3
        elif type == 'Slow':
            speed = 1
        else:
            speed = 2
        newship = Ships(ship_name = shipname, speed = speed, owner_id = user_id)
        db.session.add(newship)
        db.session.commit()
        return redirect(url_for('shiplist', user_id = user_id))
    return render_template('newship.html', form = form)

@app.route('/<int:user_id>/<int:ship_id>/sail/<int:route_id>')
def sail(user_id, ship_id, route_id):
    return f"Ship {ship_id} is now sailing on route {route_id}"

@app.route('/<int:user_id>/<int:ship_id>/shipdetails')
def shipdetails(user_id, ship_id):
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
