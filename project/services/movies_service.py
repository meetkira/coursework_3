from flask import current_app

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
        if "status" in data:
            # сортировка по году выпуска(сначала новые)
            if data.get("status") == "new":
                movies = MovieDAO(self._db_session).get_new(movies)
        if "page" in data:
            # пангинация
            limit = current_app.config["ITEMS_PER_PAGE"]
            offset = (data.get("page") - 1) * limit
            movies = MovieDAO(self._db_session).get_pages(movies, limit=limit, offset=offset)

        movies = MovieDAO(self._db_session).get_all(movies)

        return MovieSchema(many=True).dump(movies)
