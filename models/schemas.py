from marshmallow import Schema, fields, validates, ValidationError


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    user_type = fields.String(required=True)
    username = fields.String(required=True)
    password = fields.String(required=True, load_only=True)    # (load_only=True)  only the user can send the password, it should not be logged or save to file and not sent over the network again.

    @validates('user_type')
    def validate_user_type(self, value):
        if not value or value.strip() == '':
            raise ValidationError('User_type cannot be empty.')

    @validates('username')
    def validate_username(self, value):
        if not value or value.strip() == '':
            raise ValidationError('Username cannot be empty.')

    @validates('password')
    def validate_password(self, value):
        if not value or value.strip() == '':
            raise ValidationError('Password cannot be empty.')