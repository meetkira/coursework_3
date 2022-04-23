import base64
import hmac

from project.dao.user import UserDAO
from project.exceptions import ItemNotFound
from project.schemas.user import UserSchema
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

    def get_item_by_id(self, pk):
        user = UserDAO(self._db_session).get_one(pk)
        if not user:
            raise ItemNotFound
        return UserSchema().dump(user)

    def get_by_email(self, email):
        return UserDAO(self._db_session).get_by_email(email)

    def get_all(self):
        users = UserDAO(self._db_session).get_all()
        return UserSchema(many=True).dump(users)

    def create(self, data):
        data["password"] = self.get_hash(data["password"])
        return UserDAO(self._db_session).create(data=data)

    def update_password(self, data):
        user = self.get_one(data["id"])

        if not self.compare_passwords(user.password, data["old_password"]):
            return False

        user.password = self.get_hash(data.get("new_password"))

        UserDAO(self._db_session).update(user=user)

        return True

    def patch(self, data):
        user = self.get_one(data["id"])
        if "name" in data:
            user.name = data["name"]
        if "surname" in data:
            user.surname = data["surname"]
        if "favorite_genre" in data:
            user.favorite_genre = data["favorite_genre"]

        return UserDAO(self._db_session).update(user=user)

    def delete(self, uid):
        user = self.get_one(uid)
        UserDAO(self._db_session).delete(user=user)
