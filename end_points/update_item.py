from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required

from models.items import ItemModel
from services.db_services.db import db


uit = Blueprint('update_items', __name__, template_folder='templates', static_folder='static')


@uit.route('/items/<int:item_id>', methods=['PUT'])
@jwt_required()
@jwt_required(fresh=True)   # fresh token are for very important request (changing password, deleting account)
def update_item(item_id):
    item = ItemModel.query.get(item_id)
    if not item:
        return jsonify({'message': 'No item found for the given ID'}), 404

    request_data = request.get_json()
    if not request_data:
        return jsonify({'message': 'Bad request. No data provided.'}), 400

    for key, value in request_data.items():
        if hasattr(item, key):
            setattr(item, key, value)
    db.session.commit()
    return jsonify({'message': 'Item updated successfully', 'item': item.to_dict()}), 200