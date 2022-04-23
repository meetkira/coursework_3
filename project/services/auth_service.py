import calendar
import datetime

import jwt
from flask import abort, current_app

from . import UsersService
from .base import BaseService
from ..dao.user import UserDAO


class AuthService(BaseService):
    def create_user(self, data):
        user = UserDAO(self._db_session).get_by_email(data["email"])

        if user is not None:
            raise abort(409)

        UsersService(self._db_session).create(data=data)

    def generate_tokens(self, email, password, is_refresh=False):
        user = UserDAO(self._db_session).get_by_email(email)

        if user is None:
            raise abort(401)

        if not is_refresh:
            if not UsersService(self._db_session).compare_passwords(user.password, password):
                abort(400)

        data = {
            "email": user.email,
        }
        min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        data["exp"] = calendar.timegm(min30.timetuple())
        access_token = jwt.encode(data, current_app.config["SECRET_KEY"], algorithm=current_app.config["ALGO"])
        days130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
        data["exp"] = calendar.timegm(days130.timetuple())
        refresh_token = jwt.encode(data, current_app.config["SECRET_KEY"], algorithm=current_app.config["ALGO"])

        return {"access_token": access_token, "refresh_token": refresh_token}

    def approve_refresh_token(self, refresh_token):

        try:
            data = jwt.decode(refresh_token, current_app.config["SECRET_KEY"], algorithms=[current_app.config["ALGO"]])
        except Exception:
            raise abort(401)

        email = data.get("email")

        return self.generate_tokens(email, None, is_refresh=True)
