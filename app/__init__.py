from flask import request, jsonify
from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy

from instance.config import app_config
from app.invalid_usage import *

db = SQLAlchemy()
truth_values = ['True', 'true', 't', '']

def create_app(config_name):
    from app.models import Burger, Topping

    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    @app.route('/burgers/', methods=['POST'])
    def create():
        name = str(request.data.get('name', ''))
        has_bun = str(request.data.get('has_bun', '')) in truth_values
        has_patty = str(request.data.get('has_patty', '')) in truth_values

        if name:
            burger = Burger(name=name)
            burger.has_bun = has_bun
            burger.has_patty = has_patty

            for topping_name in request.data.get('toppings', ''):
                topping = Topping.query.filter_by(name=topping_name).first() \
                            or Topping(name=topping_name)

                burger.toppings.append(topping)

            burger.save()

            response = jsonify(__serialize(burger))
            response.status_code = 201

            return response

    @app.route('/burgers/', methods=['GET'])
    def index():
        burgers = Burger.get_all()

        results = [__serialize(burger) for burger in burgers]

        response = jsonify(results)
        response.status_code = 200

        return response

    @app.route('/burgers/<topping>', methods=['GET'])
    def find_burgers_by_topping(topping):
        burgers = Burger.query.join(Topping, Burger.toppings).filter(
            Topping.name == topping).all()

        results = [__serialize(burger) for burger in burgers]

        response = jsonify(results)
        response.status_code = 200

        return response

    @app.route('/burgers/<int:id>', methods=['PUT'])
    def update(id, **kwargs):
        burger = Burger.query.filter_by(id=id).first()

        if not burger:
            raise InvalidUsage('Burger not found', status_code=404)

        name = str(request.data.get('name', ''))
        has_bun = str(request.data.get('has_bun', ''))
        has_patty = str(request.data.get('has_patty', ''))
        topping_names = request.data.get('toppings', '')

        if name:
            burger.name = name
        if has_bun:
            burger.has_bun = has_bun in truth_values
        if has_patty:
            burger.has_patty = has_patty in truth_values
        if topping_names:
            burger.toppings = []

            for topping_name in request.data.get('toppings', ''):
                topping = Topping.query.filter_by(name=topping_name).first() \
                            or Topping(name=topping_name)

                burger.toppings.append(topping)

        burger.save()

        response = jsonify(__serialize(burger))
        response.status_code = 200

        return response

    @app.route('/burgers/<int:id>', methods=['DELETE'])
    def delete(id):
        burger = Burger.query.filter_by(id=id).first()

        if not burger:
            raise InvalidUsage('Burger not found', status_code=404)

        burger.delete()

        return jsonify({}), 204

    @app.errorhandler(InvalidUsage)
    def handle_invalid_usage(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    def __serialize(burger):
        return {
                'id': burger.id,
                'name': burger.name,
                'has_bun': burger.has_bun,
                'has_patty': burger.has_patty,
                'toppings': [{'name': topping.name,
                              'id': topping.id,
                              'burger_id': burger.id} for topping in burger.toppings]
                }
    return app
