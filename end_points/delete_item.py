from flask import jsonify, Blueprint
from flask_jwt_extended import jwt_required

from models.items import ItemModel
from services.db_services.db import db


dit = Blueprint('delete_items', __name__, template_folder='templates', static_folder='static')


@dit.route('/items/<int:item_id>', methods=['DELETE'])
@jwt_required()
@jwt_required(fresh=True)   # fresh token are for very important request (changing password, deleting account)
def delete_item_id(item_id):
    item = ItemModel.query.get(item_id)
    if item:
        db.session.delete(item)
        db.session.commit()
        return jsonify({'message': 'Item deleted successfully'}), 200
    else:
        return jsonify({'message': 'No item found for the given ID'}), 404