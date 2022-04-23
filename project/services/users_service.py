import base64
import hmac

from project.dao.user import UserDAO
from project.services.base import BaseService
from project.tools.security import generate_password_digest


class UsersService(BaseService):

    def get_hash(self, password):
        hash_digest = generate_password_digest(password)
        return base64.b64encode(hash_digest)

    def compare_passwords(self, password_hash, other_password):
        decoded_digest = base64.b64decode(password_hash)
        hash_digest = generate_password_digest(other_password)
        return hmac.compare_digest(decoded_digest, hash_digest)

    def get_one(self, uid):
        return UserDAO(self._db_session).get_one(uid)

    def get_by_email(self, email):
        return UserDAO(self._db_session).get_by_email(email)

    def get_all(self):
        return UserDAO(self._db_session).get_all()

    def create(self, data):
        data["password"] = self.get_hash(data["password"])
        return UserDAO(self._db_session).create(data=data)

    def update(self, data):
        user = self.get_one(data["id"])
        user.username = data.get("username")
        user.password = self.get_hash(data.get("password"))
        user.role = data.get("role")

        UserDAO(self._db_session).update(user=user)

        return UserDAO(self._db_session)

    def delete(self, uid):
        user = self.get_one(uid)
        UserDAO(self._db_session).delete(user=user)
