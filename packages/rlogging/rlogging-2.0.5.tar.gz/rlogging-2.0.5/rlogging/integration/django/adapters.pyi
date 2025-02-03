from django.core.handlers.wsgi import WSGIRequest as WSGIRequest
from django.http import HttpResponse as HttpResponse
from rlogging import HttpLoggerAdapter as HttpLoggerAdapter
from typing import Any

class DjangoLoggerAdapter(HttpLoggerAdapter):
    def request(self, request: WSGIRequest, *args: Any, **kwargs: Any) -> Any: ...
    def response(self, response: HttpResponse, *args: Any, **kwargs: Any) -> Any: ...
