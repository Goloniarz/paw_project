from flask import Flask, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_swagger_ui import get_swaggerui_blueprint

from config import Config
from models import db, Car
from resources.car_resource import CarListResource, CarResource

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
api = Api(app)

api.add_resource(CarListResource, '/cars')
api.add_resource(CarResource, '/cars/<int:car_id>')

SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Car API"
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

@app.route('/')
def home():
    return redirect('/swagger')

def create_tables_and_seed_data():
    try:
        with app.app_context():
            db.create_all()
            if Car.query.count() == 0:
                sample_cars = []
                db.session.bulk_save_objects(sample_cars)
                db.session.commit()
                print("Tables created.")
            else:
                print("Table car has got data.")
    except Exception as e:
        print(f"Error: {e}")

create_tables_and_seed_data()

if __name__ == '__main__':
    app.run(debug=True)
