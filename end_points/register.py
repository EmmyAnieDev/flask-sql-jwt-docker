from flask import Blueprint, jsonify, request
from passlib.hash import pbkdf2_sha256
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from models.schemas import UserSchema
from models.user_model import UserModel
from services.db_services.db import db

ru = Blueprint('register', __name__, template_folder='templates', static_folder='static')

user_schema = UserSchema()


@ru.route('/register', methods=['POST'])
def create_user():
    try:
        user_data = request.get_json()
    except ValidationError as err:
        return jsonify(err.messages), 400
    if 'username' not in user_data or 'password' not in user_data or 'user_type' not in user_data:
        return jsonify({'message': "Bad request. Ensure 'username', 'password' and 'user_type' are provided."}), 400

    existing_user = UserModel.query.filter_by(username=user_data['username']).first()
    if existing_user:
        return jsonify({"message": "User already exists with the provided username"}), 409

    user = UserModel(
        username=user_data['username'],
        password=pbkdf2_sha256.hash(user_data['password']),
        user_type=user_data['user_type']
    )

    try:
        db.session.add(user)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"message": "An error occurred while creating the user"}), 500

    serialized_user = user_schema.dump(user)

    return jsonify({"message": "User created successfully!", 'user': serialized_user}), 201