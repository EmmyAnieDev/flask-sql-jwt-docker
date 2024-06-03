from services.db_services.db import db


class UserModel(db.Model):
    __tableName__ = 'app_users'  # Correct attribute name for the table
    id = db.Column(db.Integer, primary_key=True)
    user_type = db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'user_type': self.user_type,
            'username': self.username,  # Correct attribute name
            'password': self.password
        }

    @property
    def is_admin(self):
        return self.user_type == 'admin'