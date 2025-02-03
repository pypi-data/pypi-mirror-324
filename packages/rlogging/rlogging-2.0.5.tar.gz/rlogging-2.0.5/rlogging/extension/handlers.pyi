from _typeshed import Incomplete
from logging import FileHandler

class DailyFileHandler(FileHandler):
    DATE_FORMAT: str
    def __init__(self, filename, *args, **kwargs) -> None: ...
    baseFilename: Incomplete
    stream: Incomplete
    def emit(self, record): ...
