from flask import Flask, Blueprint
from flask_restx import Api
from ma import ma
from db import db

from marshmallow import ValidationError


class Server():
    def __init__(self):
        self.app = Flask(__name__)
        self.bluePrint = Blueprint('api', __name__, url_prefix='/api')
        self.api = Api(self.bluePrint, doc='/doc', title='Sample Flask-RestPlus Application')
        self.app.register_blueprint(self.bluePrint)

        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.app.config['PROPAGATE_EXCEPTIONS'] = True

        self.car_ns = self.car_ns()
        self.user_ns = self.user_ns()

        super().__init__()

    def car_ns(self, ):
        return self.api.namespace(name='Cars', description='Car related operations', path='/')
    
    def user_ns(self, ):
        return self.api.namespace(name='User', description='User related operations', path='/')

    def run(self, ):
        self.app.run(
            port=5000,
            debug=True,
            host='0.0.0.0'
        )


server = Server()