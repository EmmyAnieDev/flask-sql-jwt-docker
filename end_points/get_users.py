from flask import jsonify, Blueprint

from models.schemas import UserSchema
from models.user_model import UserModel

gu = Blueprint('get_users', __name__, template_folder='templates', static_folder='static')


@gu.route('/users')
def get_users():
    users = UserModel.query.all()
    user_schema = UserSchema(many=True)
    user_data = user_schema.dump(users)
    return jsonify({'Users retrieved from database': user_data}), 201