from sqlalchemy.orm.scoping import scoped_session

from project.dao.models import User


class UserDAO:
    def __init__(self, session: scoped_session):
        self._db_session = session

    def get_one(self, uid):
        return self._db_session.query(User).filter(User.id == uid).one()

    def get_all(self):
        return self._db_session.query(User).all()

    def get_by_email(self, email):
        return self._db_session.query(User).filter(User.email == email).first()

    def create(self, data):
        user = User(**data)
        self._db_session.add(user)
        self._db_session.commit()
        return user

    def update(self, user):
        self._db_session.add(user)
        self._db_session.commit()
        return user

    def delete(self, user):
        self._db_session.delete(user)
        self._db_session.commit()
