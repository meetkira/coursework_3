import jwt
from flask import request, abort, current_app


def auth_required(func):
    def wrapper(*args, **kwargs):
        if "Authorization" not in request.headers:
            abort(401)

        data = request.headers["Authorization"]

        try:
            token_auth = data.split("Bearer ")[-1]
            jwt.decode(token_auth, current_app.config["SECRET_KEY"], algorithms=[current_app.config["ALGO"]])
        except Exception as e:
            print("JWT decode exception", e)
            abort(401)

        return func(*args, **kwargs)

    return wrapper
