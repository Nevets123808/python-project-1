from flask import redirect, request, url_for, render_template
from application import app, db
from application.models import Users, Cities, Ships, Routes
from application.forms import MakeAdminForm, NewCityForm, NewRouteForm, NewUserForm, UpdateShipForm, UpdateUserForm, NewShipForm, SailForm

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
    #If we want to restrict where new ships are built, the logic would go here:
    cities = Cities.query.all()
    city_names = [city.city_name for city in cities]
    form.city.choices = city_names
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
        
        #find the route corresponding to the city chosen:
        city = Cities.query.filter_by(city_name= form.city.data).first()
        route = Routes.query.filter_by(departing_id=city.city_id, destination_id=city.city_id).first()
        newship = Ships(ship_name = shipname, speed = speed, owner_id = user_id, route_id=route.route_id)
        db.session.add(newship)
        db.session.commit()
        return redirect(url_for('shiplist', user_id = user_id))
    return render_template('newship.html', form = form)

@app.route('/<int:user_id>/<int:ship_id>/sail', methods = ['GET','POST'])
def sail(user_id, ship_id):
    ship = Ships.query.get(ship_id)
    current_route = Routes.query.get(ship.route_id)
    #A city's port is represented by a route with the same departing and destination, therefore if ship is on such a route it is in a city 
    in_city = (current_route.departing_id == current_route.destination_id)
    if in_city:
        city = Cities.query.get(current_route.departing_id)
        form = SailForm()

        # Get the ids cities which have a route from the current city, but are not the current city, then get the names of theses cities
        routes_from = Routes.query.filter_by(departing_id = city.city_id)
        destination_ids = [route.destination_id for route in routes_from if route.destination_id != city.city_id]
        destination_names = [Cities.query.get(destination_id).city_name for destination_id in destination_ids]

        form.destination.choices=destination_names
        
        if form.validate_on_submit():
            destination_city = Cities.query.filter_by(city_name = form.destination.data).first()
            new_route = Routes.query.filter_by(departing_id = city.city_id, destination_id = destination_city.city_id).first()
            ship.route_id = new_route.route_id
            db.session.commit()
            return redirect(url_for('sail', user_id = user_id, ship_id = ship.ship_id))
        
        return render_template('setsail.html', form = form, city = city.city_name, ship = ship.ship_name)

    else:
        destination = Cities.query.get(current_route.destination_id)
        return render_template("sailing.html", ship_name = ship.ship_name, destination = destination.city_name)

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

@app.route('/admincitylist')
def admincitylist():
    cities = Cities.query.all()
    return render_template('admincitylist.html', cities = cities)

@app.route('/<int:city_id>/newroute', methods = ['GET','POST'])
def newroute(city_id):
    departing = Cities.query.get(city_id)
    # This finds all the routes that depart from the city and creates a list of their ids
    routes_from = Routes.query.filter_by(departing_id = departing.city_id).all()
    destination_ids = [route.destination_id for route in routes_from]

    # This then takes all the cities that are /not/ already destinations, and produces a list of their names
    destinations = Cities.query.filter(Cities.city_id.not_in(destination_ids)).all()
    destination_names = [city.city_name for city in destinations]
    
    form = NewRouteForm()
    form.destination.choices = destination_names
    if form.validate_on_submit():
        destination = Cities.query.filter_by(city_name = form.destination.data).first()
        route = Routes(departing_id = departing.city_id, destination_id = destination.city_id, length = form.length.data)
        #Create a route back at the same time, so routes aren't one-way
        route_back = Routes(departing_id = destination.city_id, destination_id = departing.city_id, length = form.length.data)
        db.session.add_all([route,route_back])
        db.session.commit()
        
        return redirect(url_for('admin'))
    return render_template('newroute.html', form=form, city= departing.city_name)

@app.route("/endturn")
def endturn():
    #get id for all routes that represent cities (we want to ignore these)
    city_routes = Routes.query.filter(Routes.departing_id==Routes.destination_id).all()
    city_route_ids = [route.route_id for route in city_routes]
    #get all ships which are not on city-routes, ie. those currently sailing
    ships_sailing = Ships.query.filter(Ships.route_id.not_in(city_route_ids)).all()
    for ship in ships_sailing:
        current_route = Routes.query.get(ship.route_id)
        ship.dist += ship.speed
        if ship.dist >= current_route.length:
            destination_city_id = current_route.destination_id
            destination_route = Routes.query.filter_by(departing_id = destination_city_id, destination_id = destination_city_id).first()
            ship.route_id = destination_route.route_id
        db.session.commit()
    return redirect(url_for('home'))
        