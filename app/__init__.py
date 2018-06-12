from flask import request, jsonify, abort
from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy

from instance.config import app_config

db = SQLAlchemy()
truth_values = ['True', 'true', 't', '']

def create_app(config_name):
    from app.models import Burger

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
            burger.save()
            response = __response(burger)
            response.status_code = 201
            return response

    @app.route('/burgers/', methods=['GET'])
    def index():
        # GET
        burgers = Burger.get_all()
        results = []

        for burger in burgers:
            obj = {
                'id': burger.id,
                'name': burger.name,
                'has_bun': burger.has_bun,
                'has_patty': burger.has_patty,
                'date_created': burger.date_created,
                'date_modified': burger.date_modified
            }
            results.append(obj)
        response = jsonify(results)
        response.status_code = 200
        return response

    @app.route('/burgers/<int:id>', methods=['GET', 'PUT', 'DELETE'])
    def burger_manipulation(id, **kwargs):
        # retrieve a burger using its ID
        burger = Burger.query.filter_by(id=id).first()
        if not burger:
            # Raise an HTTPException with a 404 not found status code
            abort(404)

        if request.method == 'DELETE':
            burger.delete()
            return {
                "message": "burger {} deleted successfully".format(burger.id)
            }, 200

        elif request.method == 'PUT':
            name = str(request.data.get('name', ''))
            burger.name = name
            burger.save()
            response = __response(burger)
            response.status_code = 200
            return response
        else:
            # GET
            response = __response(burger)
            response.status_code = 200
            return response

    def __response(burger):
        return jsonify({
                'id': burger.id,
                'name': burger.name,
                'has_bun': burger.has_bun,
                'has_patty': burger.has_patty,
                'date_created': burger.date_created,
                'date_modified': burger.date_modified
                })
    return app
