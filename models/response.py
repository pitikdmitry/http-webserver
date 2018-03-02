from datetime import datetime


class Response:
    # status-codes
    OK = '200 OK'
    NOT_FOUND = '404 Not Found'
    NOT_ALLOWED = '405 Method Not Allowed'
    FORBIDDEN = '403 Forbidden'
    #

    def __init__(self,
                 status_code: str,
                 protocol: str,
                 content_type: str = '',
                 content_length: int = None,
                 body: bytes = b'',
                 date: datetime = None):
        self._status_code = status_code
        self._protocol = protocol
        self._content_type = content_type
        self._content_length = content_length
        self._body = body
        self._date = date

    @property
    def status_code(self) -> str:
        return self._status_code

    @property
    def protocol(self) -> str:
        return self._protocol

    @property
    def body(self) -> bytes:
        return self._body

    @property
    def content_type(self) -> str:
        return self._content_type

    @property
    def content_length(self) -> int:
        return self._content_length

    @property
    def date(self) -> datetime:
        return self._date
