from flask import Flask
from models import db
from auth import auth_bp
from car import car_bp
from rental import rental_bp

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@db:5432/car_rental'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(car_bp)
app.register_blueprint(rental_bp)

@app.route('/')
def home():
    return "Car Rental Platform is running!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
