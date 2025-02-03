from _typeshed import Incomplete
from django.core.handlers.wsgi import WSGIRequest as WSGIRequest
from django.http import HttpResponse as HttpResponse
from rlogging.extension import namespaces as namespaces
from rlogging.integration.django.adapters import DjangoLoggerAdapter as DjangoLoggerAdapter
from rlogging.utils import LazyStrCallable as LazyStrCallable
from typing import Any

class LoggingMiddleware:
    get_response: Incomplete
    def __init__(self, get_response) -> None: ...
    def __call__(self, request: WSGIRequest): ...
    def process_view(self, request: WSGIRequest, view_func: Any, view_args: tuple, view_kwargs: dict): ...
    def process_exception(self, request, exception) -> None: ...
