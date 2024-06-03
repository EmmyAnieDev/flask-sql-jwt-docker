from flask import jsonify, Blueprint
from flask_jwt_extended import jwt_required

from models.items import ItemModel

it = Blueprint('items', __name__, template_folder='templates', static_folder='static')


@it.route('/items')
def get_items():
    items = ItemModel.query.all()    # query comes from db.Model(Flask SQLAlchemy).
    return jsonify({'all available items': [item.to_dict() for item in items]})