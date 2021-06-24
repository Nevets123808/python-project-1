from application import db
from application.models import *

db.drop_all()
db.create_all()

#create default cities
baywood = Cities(city_name = "Baywood")
mistmere = Cities(city_name = "Mistmere")
cloudharbour = Cities(city_name = "Cloudharbour")
swangulf = Cities(city_name = "Swangulf")
flatwell = Cities(city_name = "Flatwell")
db.session.add_all([baywood, mistmere, cloudharbour, swangulf, flatwell])
db.session.commit()

#city routes
cities = Cities.query.all()
city_routes = [Routes(departing_id = city.city_id, destination_id = city.city_id) for city in cities]
db.session.add_all(city_routes)
db.session.commit()

#Transit routes
routes_between = [("Baywood", "Mistmere", 10), ("Baywood", "Cloudharbour", 15), ("Mistmere","Swangulf", 10), ("MistMere", "Flatwell", 10),("Cloudharbour", "Swangulf", 5), ("Swangulf","Flatwell", 10)]
routes_to_add = []
for journey in routes_between:
    departing_city = Cities.query.filter_by(city_name = journey[0]).first()
    destination_city = Cities.query.filter_by(city_name = journey[1]).first()
    route_to_make = Routes(departing = departing_city, destination = destination_city, length = journey[2])
    route_to_make = Routes(departing = destination_city, destination = departing_city, length = journey[2])
    routes_to_add.append(route_to_make)
db.session.add_all(routes_to_add)
db.session.commit()
