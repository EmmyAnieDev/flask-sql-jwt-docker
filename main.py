from flask import Flask, request, jsonify
from services.db_services.db import *
import os
import services


db_url = ''

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = db_url or os.getenv('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = Flask
db.init_app(app)


@app.before_request
def create_table():
    db.create_all()


@app.errorhandler(404)
def not_found_error(e):
    return jsonify({'message': 'Not Found: Please check and confirm your request'}), 404


@app.errorhandler(500)
def handle_500_error(e):
    app.logger.error('Server Error: %s', e)
    return jsonify({'message': 'Internal Server Error, could not retrieve data'}), 500


@app.route('/')
def welcome():
    return 'Welcome to our store!'


@app.route('/items')
def get_items():
    return jsonify({'all available items': items})


@app.route('/items/<int:item_id>')
def get_item_id(item_id):
    if item_id in items:
        return jsonify({'item found': items[item_id], 'message': 'Data retrieved successfully'}), 200
    else:
        return jsonify({'message': 'No item found for the given ID'}), 404


@app.route('/items', methods=['POST'])
def create_item():
    request_data = request.get_json()
    if 'name' not in request_data or 'price' not in request_data:
        return jsonify({'message': "Bad request. Ensure 'name' and 'price' are included in the request."}), 400

    for item in items.values():
        if request_data['name'] == item['name']:
            return jsonify({'message': 'Bad request: Item already exists.'}), 400

    new_item_id = max(items.keys()) + 1
    new_item = {'name': request_data['name'], 'price': request_data['price']}
    items[new_item_id] = new_item
    return jsonify({'message': 'Item added successfully', 'items': items}), 201


@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item_id(item_id):
    if item_id in items:
        del items[item_id]
        return jsonify({'message': 'Item deleted successfully'}), 200
    else:
        return jsonify({'message': 'No item found for the given ID'}), 404


@app.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    if item_id not in items:
        return jsonify({'message': 'No item found for the given ID'}), 404

    request_data = request.get_json()
    if not request_data:
        return jsonify({'message': 'Bad request. No data provided.'}), 400

    item = items[item_id]
    for key, value in request_data.items():
        if key in item:
            item[key] = value
    return jsonify({'message': 'Item updated successfully', 'item': items[item_id]}), 200


if __name__ == '__main__':
    app.run(debug=True, port=5001)