from db import db
from typing import List


class CarModel(db.Model):
    __tablename__ = "cars"

    id = db.Column(db.Integer, primary_key=True)
    marca = db.Column(db.String(80), nullable=False)
    modelo = db.Column(db.String(80), nullable=False)
    ano = db.Column(db.Integer, nullable=False)
    valor = db.Column(db.String(80), nullable=False)

    def __init__(self, marca, modelo, ano, valor):
        self.marca = marca
        self.modelo = modelo
        self.ano = ano
        self.valor = valor

    def __repr__(self):
        return f'CarModel(marca={self.marca}, modelo={self.modelo}, ano={self.ano}, valor={self.valor})'

    def json(self):
        return {'marca': self.marca, 'modelo': self.modelo,'ano': self.ano, 'valor': self.valor}

    @classmethod
    def find_by_marca(cls, marca) -> List["CarModel"]:
        return cls.query.filter_by(marca=marca).all()

    @classmethod
    def find_by_marca(cls, modelo) -> List["CarModel"]:
        return cls.query.filter_by(modelo=modelo).all()

    @classmethod
    def find_by_id(cls, _id) -> "CarModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls) -> List["CarModel"]:
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()