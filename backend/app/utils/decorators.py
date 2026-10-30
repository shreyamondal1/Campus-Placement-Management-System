from flask import session
from functools import wraps
from app.database.models import User
from app.utils.errors import AuthenticationError, AuthorizationError

def login_required(function):
    @wraps(function)
    def wrapper(*args, **kwargs):

        user_id = session.get("user_id")

        if user_id is None:
            raise AuthenticationError("Authentication required.")

        user = User.query.get(user_id)

        if user is None:
            session.clear()
            raise AuthenticationError("Invalid session.")

        if user.status != "Active":
            raise AuthorizationError("Account access restricted.")

        return function(*args, **kwargs)

    return wrapper

def role_required(*roles):
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):

            user_id = session.get("user_id")

            if user_id is None:
                raise AuthenticationError("Authentication required.")

            user = User.query.get(user_id)

            if user is None:
                session.clear()
                raise AuthenticationError("Invalid session.")

            if user.status != "Active":
                raise AuthorizationError("Account access restricted.")

            if user.role not in roles:
                raise AuthorizationError("Access forbidden.")

            return function(*args, **kwargs)

        return wrapper

    return decorator
