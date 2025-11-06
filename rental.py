from flask import Blueprint, request, jsonify
from sqlalchemy.orm import joinedload
from models import db, Car, Rental
from datetime import datetime
from auth import auth

rental_bp = Blueprint('rental', __name__)

# Rent a car
@rental_bp.route('/rent', methods=['POST'])
@auth.login_required
def rent_car():
    data = request.get_json()
    car_id = data.get('car_id')

    user = auth.current_user()
    car = Car.query.get(car_id)

    if not user or user.role != 'user':
        return jsonify({'error': 'Only normal users can rent cars'}), 403

    if not car or not car.is_available:
        return jsonify({'error': 'Car not available, is already rented'}), 400

    # Check if user already rent a car
    active_rental = Rental.query.filter_by(user_id=user.id, is_active=True).first()
    if active_rental:
        return jsonify({'error': 'User already has an active rental'}), 400

    rental = Rental(
        user_id=user.id,
        car_id=car.id,
        start_date= None,
        end_date=None
    )
    car.is_available = False

    db.session.add(rental)
    db.session.commit()

    return jsonify({'message': 'Car rented successfully!'}), 201


# Return a car
@rental_bp.route('/return', methods=['POST'])
@auth.login_required
def return_car():
    user = auth.current_user()

    if not user or user.role != 'user':
        return jsonify({'error': 'Only normal users can return cars'}), 403

    rental = Rental.query.filter_by(user_id=user.id, is_active=True).first()
    if not rental:
        return jsonify({'error': 'No active rental found for this user'}), 400

    rental.end_date = datetime.utcnow()
    duration_days = (rental.end_date - rental.start_date).days + 1
    total_fee = duration_days * rental.car.daily_price
    
    rental_count = Rental.query.filter(Rental.user_id == user.id).count()

    # Determine discount rate
    if rental_count == 1:
        discount_rate = 0.1  # 10%
    elif rental_count % 10 == 0:
        discount_rate = 0.5  # 50%    
    elif rental_count % 5 == 0:
        discount_rate = 0.2  # 20%
    else:
        discount_rate = 0.0  # no discount

    total_fee = (1-discount_rate) * total_fee    

    rental.car.is_available = True    
    rental.fee = total_fee
    rental.isActive = False
    db.session.commit()

    return jsonify({
        'message': 'Car returned successfully!',
        'rental_days': duration_days,
        'daily_price': rental.car.daily_price,
        'total_price (with discount)': total_fee
    }), 200



@rental_bp.route('/rental-history', methods=['GET'])
@auth.login_required
def get_rental_history():
    user = auth.current_user()
    if not user or user.role != 'user':
        return jsonify({'error': 'Only customer users can view rental history'}), 403
    
    # I used joined load to prevent performance issues if dataset becomes larger
    rentals = Rental.query.options(
        joinedload(Rental.car).joinedload(Car.merchant)
    ).filter_by(user_id=user.id).all()

    if not rentals:
        return jsonify({'message': 'No rental history found'}), 200

    history = [
        {
            'car_id': r.car.id,
            'brand': r.car.brand,
            'model': r.car.model,
            'color': r.car.color,
            'year': r.car.year,
            'merchant_username': r.car.merchant.username,
            'start_date': r.start_date.strftime('%Y-%m-%d %H:%M:%S') if r.start_date else None,
            'end_date': r.end_date.strftime('%Y-%m-%d %H:%M:%S') if r.end_date else None,
            'is_active': r.is_active,
            'fee': r.fee
        }
        for r in rentals
    ]

    return jsonify(history), 200

