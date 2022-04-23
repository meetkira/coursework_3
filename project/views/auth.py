from flask import request, abort
from flask_restx import Resource, Namespace

from project.services import AuthService
from project.setup_db import db

auth_ns = Namespace('auth')


@auth_ns.route('/register')
class AuthRegisterView(Resource):
    def post(self):
        data = request.json
        email = data.get("email")
        password = data.get("password")

        if None in [email, password]:
            abort(400)

        AuthService(db.session).create_user(data)

        return "", 201


@auth_ns.route('/login')
class AuthLoginView(Resource):
    def post(self):
        data = request.json
        email = data.get("email")
        password = data.get("password")

        if None in [email, password]:
            abort(400)

        tokens = AuthService(db.session).generate_tokens(email=email, password=password)

        return tokens, 201

    def put(self):
        data = request.json
        refresh_token = data.get('refresh_token')
        if refresh_token is None:
            abort(400)

        tokens = AuthService(db.session).approve_refresh_token(refresh_token)

        return tokens, 201
