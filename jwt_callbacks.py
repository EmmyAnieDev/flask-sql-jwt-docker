from flask import jsonify
from models.user_model import UserModel
from blocklist import BLOCKLIST


def add_claims_to_access_token(identity):
    user = UserModel.query.filter_by(id=identity).first()
    return {'admin': user.is_admin}


def token_not_fresh_callback(jwt_header, jwt_payload):
    return jsonify({'message': 'The token is not fresh.'}), 401


def check_if_token_in_blocklist(jwt_header, jwt_payload):
    return jwt_payload['jti'] in BLOCKLIST


def revoked_token_callback(jwt_header, jwt_payload):
    return jsonify({'message': 'error: the token has been revoked'}), 401


def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({'message': 'The token has expired.', 'error': 'token_expired'}), 401


def invalid_token_callback(error):
    return jsonify({'message': 'The token is invalid.', 'error': 'invalid_token'}), 422


def unauthorized_callback(error):
    return jsonify({'message': 'Request does not contain an access token.', 'error': 'authorization_required'}), 401