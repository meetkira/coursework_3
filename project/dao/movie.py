from sqlalchemy.orm.scoping import scoped_session

from project.dao.models import Movie


class MovieDAO:
    def __init__(self, session: scoped_session):
        self._db_session = session

    def get_by_id(self, pk):
        return self._db_session.query(Movie).filter(Movie.id == pk).one_or_none()

    def get_movies(self):
        return self._db_session.query(Movie)

    def get_all(self, movies_query):
        return movies_query.all()

    def get_new(self, movies_query):
        return movies_query.order_by(Movie.year.desc())

    def get_pages(self, movies_query, limit, offset):
        return movies_query.limit(limit).offset(offset)
