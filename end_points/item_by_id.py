from flask import jsonify, Blueprint
from models.items import ItemModel

itd = Blueprint('items_id', __name__, template_folder='templates', static_folder='static')


@itd.route('/items/<int:item_id>')
def get_item_id(item_id):
    item = ItemModel.query.get_or_404(item_id)
    return jsonify({'item found': item.to_dict(), 'message': 'Data retrieved successfully'}), 200