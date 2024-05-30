#!/usr/bin/env python3
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)


@app.route("/")
def index():
    return "<h1>Code challenge</h1>"

@app.get('/restaurants')
def get_rest():
    return [r.to_dict(rules=["-restaurant_pizzas"]) for r in Restaurant.query.all()], 200

@app.get('/restaurants/<int:id>')
def get_rest_by_id(id):
    restaurant = Restaurant.query.get(id)
    if restaurant:
        return restaurant.to_dict(), 200
    else:
        return {"error": "Restaurant not found"}, 404
    
@app.delete('/restaurants/<int:id>')
def delete_rest(id):
    restaurant = Restaurant.query.get(id)
    if restaurant:
        db.session.delete(restaurant)
        db.session.commit()
        return {}, 204
    else:
        return {"error": "Restaurant not found"}, 404

@app.get('/pizzas')
def get_pizza():
    return [p.to_dict(rules=["-restaurant_pizzas"]) for p in Pizza.query.all()], 200

@app.post('/restaurant_pizzas')
def post_rest_pizza():
    try:
        new_rest_pizza = RestaurantPizza(
            price=request.json['price'],
            pizza_id=request.json['pizza_id'],
            restaurant_id=request.json['restaurant_id']
        )
        db.session.add(new_rest_pizza)
        db.session.commit()
        return new_rest_pizza.to_dict(), 201
    except Exception as e:
        return {"errors": ["validation errors"]}, 400

if __name__ == "__main__":
    app.run(port=5555, debug=True)