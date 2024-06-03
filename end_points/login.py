from flask import Blueprint, jsonify, request
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity
from models.schemas import UserSchema
from models.user_model import UserModel

lg = Blueprint('login', __name__, template_folder='templates', static_folder='static')

user_schema = UserSchema()


@lg.route('/login', methods=['POST'])
def login():
    provided_username = request.json.get('username')
    provided_password = request.json.get('password')

    if not provided_username or not provided_password:
        return jsonify({'message': 'Username and password are required.'}), 400

    user = UserModel.query.filter_by(username=provided_username).first()

    if not user or not pbkdf2_sha256.verify(provided_password, user.password):
        return jsonify({'message': 'Invalid username or password.'}), 401

    access_token = create_access_token(identity=user.id, fresh=True)  # use fresh equals true
    refresh_token = create_refresh_token(identity=user.id)  # use when requesting refresh endpoints
    serialized_user = user_schema.dump(user)

    return jsonify({'message': 'Login successful!', 'user_id': serialized_user, 'access_token': access_token, 'refresh_token': refresh_token}), 200