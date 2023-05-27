from django.db.backends.utils import CursorWrapper
from django.db import connection


class QueryInterceptingCursorWrapper(CursorWrapper):
    def execute(self, sql, params=None):

        # Esegui la query manipolata
        return super().execute(sql, params)


class QueryInterceptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Prima dell'esecuzione della vista
        connection.cursor_wrapper = QueryInterceptingCursorWrapper
        response = self.get_response(request)

        # Dopo l'esecuzione della vista

        return response
