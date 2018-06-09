from flask import request, jsonify, abort
from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy

from instance.config import app_config

db = SQLAlchemy()

def create_app(config_name):
    from app.models import Burger

    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    @app.route('/burgers/', methods=['POST', 'GET'])
    def burgers():
        if request.method == 'POST':
            name = str(request.data.get('name', ''))
            if name:
                burger = Burger(name=name)
                burger.save()
                response = jsonify({
                    'id': burger.id,
                    'name': burger.name,
                    'date_created': burger.date_created,
                    'date_modified': burger.date_modified
                })
                response.status_code = 201
                return response
        else:
            # GET
            burgers = Burger.get_all()
            results = []

            for burger in burgers:
                obj = {
                    'id': burger.id,
                    'name': burger.name,
                    'date_created': burger.date_created,
                    'date_modified': burger.date_modified
                }
                results.append(obj)
            response = jsonify(results)
            response.status_code = 200
            return response
    return app
