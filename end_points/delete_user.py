from flask import jsonify, Blueprint
from flask_jwt_extended import jwt_required, get_jwt

from models.user_model import UserModel
from services.db_services.db import db

duid = Blueprint('delete_user', __name__, template_folder='templates', static_folder='static')


@duid.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
@jwt_required(fresh=True)   # fresh token are for very important request (changing password, deleting account)
def delete_user_id(user_id):
    claims = get_jwt()
    if not claims.get('admin'):
        return jsonify({'message': 'Admins only!'}), 403

    user = UserModel.query.get_or_404(user_id)
  #  if user:
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'}), 200
    # else:
    #     return jsonify({'message': 'No item found for the given ID'}), 404