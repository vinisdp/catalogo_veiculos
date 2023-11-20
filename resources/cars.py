from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required, verify_jwt_in_request
from flask_restx import Resource, fields

from models.cars import CarModel
from schemas.cars import CarSchema

from server.instance import server

ITEM_NOT_FOUND = "Car not found."

car_ns = server.car_ns
car_schema = CarSchema()
car_list_schema = CarSchema(many=True)

# Model required by flask_restx for expect
item = car_ns.model('Car', {
    'marca': fields.String('Marca do carro'),
    'modelo': fields.String('Modelo do carro'),
    'ano': fields.Integer(0),
    'valor': fields.String('Valor do carro'),
    'imagem': fields.String('Imagem do carro'),
})

@car_ns.route('/cars/<int:id>')
class Car(Resource):

    def get(self, id):
        car_data = CarModel.find_by_id(id)
        if car_data:
            return car_schema.dump(car_data)
        return {'message': ITEM_NOT_FOUND}, 404

    def delete(self, id):
        car_data = CarModel.find_by_id(id)
        if car_data:
            car_data.delete_from_db()
            return '', 204
        return {'message': ITEM_NOT_FOUND}, 404

    @car_ns.expect(item)
    def put(self, id):
        car_data = CarModel.find_by_id(id)
        car_json = request.get_json()

        if car_data:
            car_data.marca = car_json['marca']
            car_data.modelo = car_json['modelo']
            car_data.ano = car_json['ano']
            car_data.valor = car_json['valor']
            car_data.imagem = car_json['imagem']
            
        else:
            car_data = car_schema.load(car_json)

        car_data.save_to_db()
        return car_schema.dump(car_data), 200

@car_ns.route('/cars')
class CarList(Resource):
    @car_ns.doc('Get all the Items')
    def get(self):
        current_user_id = get_jwt_identity()
        print(current_user_id)
        return car_list_schema.dump(CarModel.find_all()), 200
    
    
    @car_ns.expect(item)
    @car_ns.doc('Create an Item')
    @jwt_required()
    def post(self):
        
        
        
        car_json = request.get_json()
        car_data = car_schema.load(car_json)

        car_data.save_to_db()

        return car_schema.dump(car_data), 201