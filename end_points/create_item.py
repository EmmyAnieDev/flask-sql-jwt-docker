from sqlite3 import IntegrityError
from flask import request, jsonify, Blueprint
from flask_jwt_extended import jwt_required

from models.items import ItemModel
from services.db_services.db import db


pit = Blueprint('post_items', __name__, template_folder='templates', static_folder='static')


@pit.route('/items', methods=['POST'])
@jwt_required()
def create_item():
    item_data = request.get_json()
    if 'name' not in item_data or 'price' not in item_data:
        return jsonify({'message': "Bad request. Ensure 'name' and 'price' are included in the request."}), 400

    item = ItemModel(**item_data)
    db.session.add(item)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({'message': 'An item with this name already exists.'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f"An error occurred: {e}"}), 500
    return jsonify({'message': 'Item added successfully', 'item': item.to_dict()}), 201   # remember to return just the 'message' during production