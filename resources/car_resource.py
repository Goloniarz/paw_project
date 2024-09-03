from flask import request, jsonify
from flask_restful import Resource
from models import db, Car

class CarListResource(Resource):
    def get(self):
        cars = Car.query.all()
        return jsonify([{
            'id': car.id,
            'brand': car.brand,
            'model': car.model,
            'price': car.price,
            'power': car.power,
            'color': car.color
        } for car in cars])

    def post(self):
        new_car = Car(
            brand=request.json['brand'],
            model=request.json['model'],
            price=request.json['price'],
            power=request.json['power'],
            color=request.json['color']
        )
        db.session.add(new_car)
        db.session.commit()
        return jsonify({'message': 'Car added successfully!'})

class CarResource(Resource):
    def get(self, car_id):
        car = Car.query.get_or_404(car_id)
        return jsonify({
            'id': car.id,
            'brand': car.brand,
            'model': car.model,
            'price': car.price,
            'power': car.power,
            'color': car.color
        })

    def put(self, car_id):
        car = Car.query.get_or_404(car_id)
        car.brand = request.json['brand']
        car.model = request.json['model']
        car.price = request.json['price']
        car.power = request.json['power']
        car.color = request.json['color']
        db.session.commit()
        return jsonify({'message': 'Car updated successfully!'})

    def delete(self, car_id):
        car = Car.query.get_or_404(car_id)
        db.session.delete(car)
        db.session.commit()
        return jsonify({'message': 'Car deleted successfully!'})
