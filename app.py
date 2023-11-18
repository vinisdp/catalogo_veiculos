from flask import Flask, Blueprint, jsonify
import werkzeug
werkzeug.cached_property = werkzeug.utils.cached_property
from werkzeug.utils import cached_property
from flask_restx import Api
from ma import ma
from db import db

from resources.cars import Car, CarList, car_ns
from marshmallow import ValidationError

from server.instance import server

api = server.api
app = server.app





@api.errorhandler(ValidationError)
def handle_validation_error(error):
    return jsonify(error.messages), 400


if __name__ == '__main__':
    db.init_app(app)
    ma.init_app(app)
    with app.app_context():
        # Cria as tabelas no banco de dados antes de iniciar o servidor
        db.create_all()
    server.run()
