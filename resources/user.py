# routes/user_routes.py
from flask import request
from flask_restx import Resource, fields
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash
from models.user import UserModel

from server.instance import server

user_ns = server.user_ns

user_model = user_ns.model('User', {
    'username': fields.String(description='Nome de usuário'),
    'password': fields.String(description='Senha do usuário'),
})

@user_ns.route('/users/login')
class UserLogin(Resource):
    @user_ns.expect(user_model)
    @user_ns.doc('login_user')
    def post(self):
        if not request.is_json:
            return {'message': 'Conteúdo inválido'}, 400

        username = request.json.get('username')
        password = request.json.get('password')

        user = UserModel.query.filter_by(username=username).first()

        if user and user.check_password(password):
            access_token = create_access_token(identity=user.username)
            return {'access_token': access_token}, 200
        else:
            return {'message': 'Credenciais inválidas'}, 401
