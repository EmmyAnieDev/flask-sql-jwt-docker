from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt

from blocklist import BLOCKLIST

lgt = Blueprint('logout', __name__, template_folder='templates', static_folder='static')


@lgt.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    # Blacklist the current token
    jti = get_jwt()['jti']
    BLOCKLIST.add(jti)
    return jsonify({'message': 'Logged out successfully'}), 200