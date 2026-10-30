from flask_restx import fields

register_fields = {
    "username": fields.String(required=True),
    "email": fields.String(required=True),
    "password": fields.String(required=True),
    "role": fields.String(required=True)
}

login_fields = {
    "username_or_email": fields.String(required=True),
    "password": fields.String(required=True),
    "role": fields.String(required=True)
}

user_fields = {
    "id": fields.Integer,
    "username": fields.String,
    "email": fields.String,
    "role": fields.String,
    "status": fields.String
}
