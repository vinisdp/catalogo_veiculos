# routes/user_routes.py
from flask import jsonify, redirect, request, url_for
from flask_restx import Resource, fields
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, set_access_cookies
from werkzeug.security import check_password_hash
from models.user import UserModel
from schemas.user import UserSchema
from flask_jwt_extended import unset_jwt_cookies
import hashlib
import time

from server.instance import server

user_ns = server.user_ns
user_schema = UserSchema()
user_list_schema = UserSchema(many=True)

user_create_model = user_ns.model('UserCreate', {
    'username': fields.String(description='Nome de usuário'),
    'name': fields.String(description='Nome'),
    'password': fields.String(description='Senha do usuário'),
    'email': fields.String(description='Email'),
})
user_login_model = user_ns.model('User', {
    'username': fields.String(description='Nome de usuário'),
    'password': fields.String(description='Senha do usuário'),
})

@user_ns.route('/users/login')
class UserLogin(Resource):
    @user_ns.expect(user_login_model)
    @user_ns.doc('login_user')
    def post(self):
        if not request.is_json:
            return {'message': 'Conteúdo inválido'}, 400

        username = request.json.get('username')
        password = request.json.get('password')

        user = UserModel.query.filter_by(username=username).first()
        print(user.password)
        response = jsonify({"msg": "Login successful"})
        if user and check_password(user.password, password):
            access_token = create_access_token(identity=user.username)
            set_access_cookies(response, access_token)
            return {'access_token': access_token}, 200
        else:
            return {'message': 'Credenciais inválidas'}, 401


@user_ns.route('/users/register')
class UserRegister(Resource):

    @user_ns.doc('Get all the Items')
    def get(self):
        return user_list_schema.dump(UserModel.find_all()), 200

    @jwt_required()    
    @user_ns.expect(user_create_model)
    @user_ns.doc('Create an User')
    def post(self):
        user_json = request.get_json()
        user_data = user_schema.load(user_json)

        # Concatene a senha com o salt e aplique hash SHA-256
        hashed_password = generate_password(user_data.password)
        user_data.password = hashed_password
        user_data.save_to_db()

        return user_schema.dump(user_data), 201
    
#cria o hash da senha para transacoes
def generate_password(password):
    return hashlib.sha256((password).encode('utf-8')).hexdigest()

#checa os hashs na autenticacao
def check_password(saved_password, provided_password):
    provided_password = generate_password(provided_password)
    return saved_password == provided_password
    # Use a função de comparação do Flask-WTF (check_password_hash) se preferir
    # return check_password_hash(saved_password, provided_password)