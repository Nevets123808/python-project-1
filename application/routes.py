from flask import redirect, request, url_for, render_template
from application import app, db
from application.models import Users, Cities, Ships, Routes
from application.forms import MakeAdminForm, NewCityForm, NewUserForm, UpdateShipForm, UpdateUserForm, NewShipForm

@app.route('/')
@app.route('/home')
def home():
    users = Users.query.all()
    return render_template('home.html', users=users)

# @app.route('/selectuser/<int:user_id>')
# def selectuser(user_id):
#     return f"You are now using user {user_id}"

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
    ship = Ships.query.get(ship_id)
    city = None
    return render_template('ship.html', user_id = user_id, ship = ship, city = city)

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

@app.route('/<int:user_id>/<int:ship_id>/shipdetails', methods = ['GET','POST'])
def shipdetails(user_id, ship_id):
    form = UpdateShipForm()
    ship = Ships.query.get(ship_id)
    if form.validate_on_submit():
        if form.name.data:
            ship.ship_name = form.name.data
            db.session.commit()
        return redirect(url_for('ship', user_id = user_id, ship_id = ship.ship_id))
    return render_template('updateship.html', form = form, ship = ship)

@app.route('/<int:user_id>/<int:ship_id>/deleteship')
def deleteship(user_id, ship_id):
    ship_to_delete = Ships.query.get(ship_id)
    db.session.delete(ship_to_delete)
    db.session.commit()
    return redirect(url_for('shiplist', user_id = user_id))

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/makeadmin', methods = ['GET','POST'])
def makeadmin():
    form = MakeAdminForm()

    # To allow dynamic options, we "rebuild" the user field of the MakeAdminForm
    # so the choices reflect the actual state of the db
    users = Users.query.filter_by(admin=False).all()
    usernames = [user.username for user in users]
    form.user.choices = usernames

    if form.validate_on_submit():
        user = Users.query.filter_by(username = form.user.data).first()
        user.admin = True
        db.session.commit()
        return redirect(url_for('admin'))
    return render_template('makeadmin.html', form = form)

@app.route('/newcity', methods = ['GET','POST'])
def newcity():
    form = NewCityForm()
    if form.validate_on_submit():
        print("hello!")
        city = Cities(city_name=form.name.data)
        db.session.add(city)
        db.session.commit()

        #We also need the route representing the cities port
        city = Cities.query.filter_by(city_name = form.name.data).first()
        route = Routes(departing_id = city.city_id, destination_id = city.city_id, length = 0)
        db.session.add(route)
        db.session.commit()

        return redirect(url_for('admin'))
    return render_template('newcity.html', form = form)

@app.route('/newroute')
def newroute():
    return "You have made a new route"
