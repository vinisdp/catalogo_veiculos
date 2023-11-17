from ma import ma
from models.cars import CarModel


class CarSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CarModel
        load_instance = True

