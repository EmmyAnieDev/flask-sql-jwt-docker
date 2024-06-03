from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required, create_access_token, get_jwt

from blocklist import BLOCKLIST

rf = Blueprint('refresh', __name__, template_folder='templates', static_folder='static')


@rf.route('/refresh')
@jwt_required(refresh=True)   # means needs a refresh token not an access token
def refresh_token():
    current_user = get_jwt_identity()
    new_token = create_access_token(identity=current_user, fresh=False)   # everytime access token expires, the client will generate a new access token use the /refresh endpoint
    # to generate just one FRESH TOKEN for every REFRESH TOKEN
    # jti = get_jwt()['jti']
    # BLOCKLIST.add(jti)
    return jsonify({'access_token': new_token}), 200