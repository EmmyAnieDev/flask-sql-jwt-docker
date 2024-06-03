from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required, get_jwt

from models.schemas import UserSchema
from models.user_model import UserModel
from services.db_services.db import db
from passlib.hash import pbkdf2_sha256

upuid = Blueprint('update_user', __name__, template_folder='templates', static_folder='static')

user_schema = UserSchema()


@upuid.route('/users/<int:user_id>', methods=['PUT'])
@jwt_required()
@jwt_required(fresh=True)   # fresh token are for very important request (changing password, deleting account)
def update_user(user_id):
    claims = get_jwt()
    if not claims.get('admin'):
        return jsonify({'message': 'Admins only!'}), 403

    user = UserModel.query.get(user_id)
    if not user:
        return jsonify({'message': 'No user found for the given ID'}), 404

    user_data = request.get_json()
    if not user_data:
        return jsonify({'message': 'Bad request. No data provided.'}), 400

    if 'password' in user_data:
        user.password = pbkdf2_sha256.hash(user_data['password'])

    for key, value in user_data.items():
        if hasattr(user, key) and key != 'password':
            setattr(user, key, value)

    serialized_user = user_schema.dump(user)

    db.session.commit()
    return jsonify({'message': 'User updated successfully', 'user': serialized_user}), 200