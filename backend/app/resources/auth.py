from flask import request, session
from flask_restx import Namespace, Resource, fields
from app.database.models import User
from app.schemas.auth import register_fields, login_fields, user_fields
from app.services.auth import register_user, login_user
from app.utils.decorators import login_required

auth = Namespace("auth", path="/auth")

register_model = auth.model("Register", register_fields)
login_model = auth.model("Login", login_fields)

user_model = auth.model("User", user_fields)
auth_response_model = auth.model("AuthResponse", 
    {
        "message": fields.String,
        "user": fields.Nested(user_model)
    }
)

@auth.route("/register")
class RegisterResource(Resource):

    @auth.expect(register_model, validate=True)
    @auth.marshal_with(auth_response_model, code=201)

    def post(self):

        data = request.get_json()

        user = register_user(
            username=data["username"],
            email=data["email"],
            password=data["password"],
            role=data["role"]
        )

        return {"message": "Registration successful.", "user": user}, 201

@auth.route("/login")
class LoginResource(Resource):

    @auth.expect(login_model, validate=True)
    @auth.marshal_with(auth_response_model, code=200)

    def post(self):

        data = request.get_json()

        user = login_user(
            username_or_email=data["username_or_email"],
            password=data["password"],
            role=data["role"]
        )

        session.permanent = True
        session["user_id"] = user.id

        return {"message": "Login successful.", "user": user}, 200

@auth.route("/logout")
class LogoutResource(Resource):

    def post(self):

        session.clear()

        return {"message": "Logout successful."}, 200

@auth.route("/current_user")
class CurrentUserResource(Resource):

    @login_required
    @auth.marshal_with(user_model, code=200)
    
    def get(self):

        user_id = session.get("user_id")
        user = User.query.get(user_id)

        return user, 200
