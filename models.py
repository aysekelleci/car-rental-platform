from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'merchant' or 'user'
    rentals = db.relationship('Rental', back_populates='user')
    cars = db.relationship('Car', back_populates='merchant')  # only for role='merchant'


class Car(db.Model):
    __tablename__ = 'cars'
    id = db.Column(db.Integer, primary_key=True)
    merchant_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    brand = db.Column(db.String(50))
    model = db.Column(db.String(50))
    color = db.Column(db.String(50))
    year = db.Column(db.Integer)
    daily_price = db.Column(db.Integer, default=50) # dollar based
    is_available = db.Column(db.Boolean, default=True)

    merchant = db.relationship('User', back_populates='cars')
    rentals = db.relationship('Rental', back_populates='car')


class Rental(db.Model):
    __tablename__ = 'rentals'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    car_id = db.Column(db.Integer, db.ForeignKey('cars.id'), nullable=False)
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    end_date = db.Column(db.DateTime, nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    fee = db.Column(db.Float, default=50)

    user = db.relationship('User', back_populates='rentals')
    car = db.relationship('Car', back_populates='rentals')
