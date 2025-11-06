from flask import Blueprint, request, jsonify
from models import User, db, Car
from auth import auth

car_bp = Blueprint('cars', __name__)

# Add a new car
@car_bp.route('/cars', methods=['POST'])
@auth.login_required
def add_car():
    data = request.get_json()
    brand = data.get('brand')
    model = data.get('model')
    year = data.get('year')
    color = data.get('color')
    price = data.get('daily_price')

    merchant = auth.current_user()
    if not merchant or merchant.role != 'merchant':
        return jsonify({'error': 'Only merchants can add cars'}), 403

    car = Car(merchant_id=merchant.id, brand=brand, model=model, year=year, color=color, daily_price=price)
    db.session.add(car)
    db.session.commit()

    return jsonify({'message': 'Car added successfully!'}), 201

# Get merchant's cars
@car_bp.route('/cars', methods=['GET'])
@auth.login_required
def get_cars():
    merchant = auth.current_user()
    if not merchant or merchant.role != 'merchant':
        return jsonify({'error': 'Only merchants can list their cars'}), 403
    
    # first option:  
    cars = Car.query.filter_by(merchant_id=merchant.id).all()
    # also we can use:
    # cars = merchant.cars

    car_list = [
        {
            'id': c.id,
            'brand': c.brand,
            'model': c.model,
            'year': c.year,
            'color': c.year,
            'daily_price': c.daily_price,
            'is_available': c.is_available
        }
        for c in cars
    ]
    return jsonify(car_list)


# Update a car (merchant only)
@car_bp.route('/cars/<int:car_id>', methods=['PUT'])
@auth.login_required
def update_car(car_id):
    data = request.get_json()
    car = Car.query.get(car_id)
    if not car:
        return jsonify({'error': 'Car not found'}), 404

    merchant = auth.current_user()
    if not merchant or merchant.role != 'merchant':
        return jsonify({'error': 'Only merchants can update cars'}), 403
    if merchant.id != car.merchant_id:
        return jsonify({'error': 'You can only update your own cars'})

    car.brand = data.get('brand', car.brand)
    car.model = data.get('model', car.model)
    car.year = data.get('year', car.year)
    car.color = data.get('color', car.color)
    car.daily_price = data.get('daily_price', car.daily_price)
    db.session.commit()

    return jsonify({'message': 'Car updated successfully!'}), 200


# Delete a car (merchant only)
@car_bp.route('/cars/<int:car_id>', methods=['DELETE'])
@auth.login_required
def delete_car(car_id):
    merchant = auth.current_user()

    if not merchant or merchant.role != 'merchant':
        return jsonify({'error': 'Only merchants can delete cars'}), 403
    if merchant.id != car.merchant_id:
        return jsonify({'error': 'You can only delete your own cars'})

    car = Car.query.get(car_id)
    if not car:
        return jsonify({'error': 'Car not found'}), 404

    db.session.delete(car)
    db.session.commit()

    return jsonify({'message': 'Car deleted successfully!'}), 200



@car_bp.route('/filter-cars', methods=['POST'])
def filter_cars():
    data = request.get_json()
    brand = data.get('brand')
    model = data.get('model')
    min_year = data.get('min_year')
    max_year = data.get('max_year')
    min_price = data.get('min_price')
    max_price = data.get('max_price')
    merchant_username = data.get('merchant_username')
    color = data.get('color')
    is_available = data.get('available')

    query = Car.query
    if merchant_username:
        merchant = User.query.filter_by(username=merchant_username, role='merchant').first()
        if merchant:
            query = query.filter(Car.merchant_id == merchant.id)
        else:
            return jsonify({'error': 'Merchant not found'}), 404

    if brand:
        query = query.filter(Car.brand.ilike(f'%{brand}%'))
    if model: 
        query = query.filter(Car.model.ilike(f'%{model}%'))    
    if min_year:
        query = query.filter(Car.year >= min_year)
    if max_year:
        query = query.filter(Car.year <= max_year)
    if min_price:
        query = query.filter(Car.daily_price >= min_price)
    if max_price:
        query = query.filter(Car.daily_price <= max_price)
    if color:
        query = query.filter(Car.color.ilike(f'%{color}%'))
    if is_available is not None:
        query = query.filter(Car.is_available == is_available)    

    cars = query.all()

    results = [
        {
            'id': car.id,
            'merchant_name': car.merchant.username,
            'brand': car.brand,
            'model': car.model,
            'year': car.year,
            'daily_price': float(car.daily_price),
            'is_available': car.is_available
        }
        for car in cars
    ]

    return jsonify(results), 200




