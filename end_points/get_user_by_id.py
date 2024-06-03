from flask import jsonify, Blueprint

from models.schemas import UserSchema
from models.user_model import UserModel

guid = Blueprint('get_user_by_id', __name__, template_folder='templates', static_folder='static')


@guid.route('/users/<int:user_id>')
def get_users_by_id(user_id):
    user = UserModel.query.get_or_404(user_id)
    user_schema = UserSchema()
    user_data = user_schema.dump(user)
    return jsonify({'Users retrieved from database': user_data}), 201