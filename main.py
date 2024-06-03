import os

from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

from services.db_services.db import db

from end_points.delete_item import dit
from end_points.item_by_id import itd
from end_points.items import it
from end_points.create_item import pit
from end_points.update_item import uit
from end_points.register import ru
from end_points.get_users import gu
from end_points.get_user_by_id import guid
from end_points.delete_user import duid
from end_points.update_user import upuid
from end_points.login import lg
from end_points.logout import lgt
from end_points.refresh import rf

import jwt_callbacks as jwt_cb
import error_handlers as eh


db_url = ''

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = db_url or os.getenv('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
migrate = Migrate(app, db)   # add below [db.init_app(app)]   commands 'flask db init' then delete data.db, 'flask db migrate' 'flask db upgrade'

# command ==>  python, import secrets, secrets.SystemRandom().getrandbits(120)
app.config['JWT_SECRET_KEY'] = '447310468884973093771474415448469063'  # This is used so that when a user sends back a JWT to verify who they are, our app can check the secret key and can use it to verify that this app generated the JWT and therefore the JWT is valid.
jwt = JWTManager(app)


# Set the JWT callbacks
jwt.additional_claims_loader(jwt_cb.add_claims_to_access_token)
jwt.token_in_blocklist_loader(jwt_cb.check_if_token_in_blocklist)
jwt.revoked_token_loader(jwt_cb.revoked_token_callback)
jwt.needs_fresh_token_loader(jwt_cb.token_not_fresh_callback)
jwt.expired_token_loader(jwt_cb.expired_token_callback)
jwt.invalid_token_loader(jwt_cb.invalid_token_callback)
jwt.unauthorized_loader(jwt_cb.unauthorized_callback)


app.register_blueprint(it, url_prefix='')
app.register_blueprint(itd, url_prefix='')
app.register_blueprint(pit, url_prefix='')
app.register_blueprint(dit, url_prefix='')
app.register_blueprint(uit, url_prefix='')
app.register_blueprint(ru, url_prefix='')
app.register_blueprint(gu, url_prefix='')
app.register_blueprint(guid, url_prefix='')
app.register_blueprint(duid, url_prefix='')
app.register_blueprint(upuid, url_prefix='')
app.register_blueprint(lg, url_prefix='')
app.register_blueprint(lgt, url_prefix='')
app.register_blueprint(rf, url_prefix='')

app.errorhandler(400)(eh.handle_400_error)
app.errorhandler(401)(eh.handle_401_error)
app.errorhandler(403)(eh.handle_403_error)
app.errorhandler(404)(eh.handle_404_error)
app.errorhandler(405)(eh.handle_405_error)
app.errorhandler(409)(eh.handle_409_error)
app.errorhandler(429)(eh.handle_429_error)
app.errorhandler(500)(eh.handle_500_error)


@app.before_request
def create_table():
    db.create_all()


@app.route('/')
def welcome():
    return 'Welcome to our store!'


if __name__ == '__main__':
    app.run(debug=True, port=5001)