from flask import request
from flask_restx import abort, Namespace, Resource

from project.exceptions import ItemNotFound
from project.services import UsersService
from project.setup_db import db
from project.tools.decorators import auth_required

users_ns = Namespace("user")


@users_ns.route("/<int:user_id>")
class UserView(Resource):
    @auth_required
    @users_ns.response(200, "OK")
    @users_ns.response(404, "User not found")
    def get(self, user_id: int):
        """Get user data"""
        try:
            return UsersService(db.session).get_item_by_id(user_id)
        except ItemNotFound:
            abort(404, message="User not found")

    @auth_required
    @users_ns.response(204, "OK")
    @users_ns.response(404, "User not found")
    def patch(self, user_id: int):
        """Update user data"""
        # try:
        data = request.json
        if "id" not in data:
            data["id"] = user_id
        UsersService(db.session).patch(data)
        return "", 204
# except Exception:
# return "", 404


@users_ns.route("/<int:user_id>/password")
class UserPasswordView(Resource):
    @auth_required
    @users_ns.response(204, "OK")
    @users_ns.response(404, "User not found")
    @users_ns.response(400, "Bad request")
    def put(self, user_id: int):
        """Update user password"""
        data = request.json
        if "id" not in data:
            data["id"] = user_id

        try:
            UsersService(db.session).get_one(user_id)
        except ItemNotFound:
            abort(404, message="User not found")

        old_password = data.get("old_password")
        new_password = data.get("new_password")

        if None in [old_password, new_password]:
            abort(400)

        if not UsersService(db.session).update_password(data):
            abort(403)

        return "", 204
