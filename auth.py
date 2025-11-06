from flask import Blueprint, request, jsonify
from flask_httpauth import HTTPBasicAuth
from models import db, User

auth_bp = Blueprint('auth', __name__)
auth = HTTPBasicAuth()

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    role = data.get('role', 'user')

    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already exists'}), 400

    user = User(username=username, password=password, role=role)
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': f'User {username} registered successfully!'}), 201


@auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username=username).first()
    if user and user.password == password:
        return user
    return None


@auth_bp.route('/login')
@auth.login_required
def login():
    user = auth.current_user()
    return jsonify({
        'message': f'Welcome {user.username}!',
        'role': user.role
    }), 200


@auth_bp.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    user_list = [
        {
            'id': u.id,
            'username': u.username,
            'role': u.role
        }
        for u in users
    ]
    return jsonify(user_list), 200
