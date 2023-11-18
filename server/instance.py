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
        self.app.config["JWT_ALGORITHM"] = "HS256"
        self.app.config["JWT_SECRET_KEY"] = "26361e7fcb00fda02dadffd793fdd70702306b2608ed28e96fe0a0e45b696d8a"
        self.app.config["SECRET_KEY"] = "2eecdae4c7866551d62fa910051fb6658ff347bf5ef1da64d3adda7899e01df4"
        self.app.config["JWT_REFRESH_TOKEN_EXPIRES"] = 30
        self.app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 20
        self.app.config['JWT_TOKEN_LOCATION'] = ['cookies']
        self.app.config['JWT_SESSION_COOKIE'] = True

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