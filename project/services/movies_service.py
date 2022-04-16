from project.dao import MovieDAO
from project.exceptions import ItemNotFound
from project.schemas.movie import MovieSchema
from project.services.base import BaseService


class MoviesService(BaseService):
    def get_item_by_id(self, pk):
        movie = MovieDAO(self._db_session).get_by_id(pk)
        if not movie:
            raise ItemNotFound
        return MovieSchema().dump(movie)

    def get_all_movies(self, data):

        movies = MovieDAO(self._db_session).get_movies()
        if data["status"] == "new":
            movies = MovieDAO(self._db_session).get_new(movies)
        if data["page"]:
            # пангинация
            movies = MovieDAO(self._db_session).get_pages(movies, limit=data["page"])

        movies = MovieDAO(self._db_session).get_all(movies)

        return MovieSchema(many=True).dump(movies)
