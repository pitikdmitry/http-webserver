from datetime import datetime

from models.response_head import ResponseHead


class ResponseGet(ResponseHead):

    today_date = datetime.today()

    def __init__(self, status_code: str,
                 protocol: str,
                 content_type: str = '',
                 content_length=None,
                 body=None,
                 connection=None):
        super().__init__(status_code, protocol, connection)

        self._content_type = content_type
        self._content_length = content_length
        self._body = body
        self._server = "server"
        self._date = ResponseGet.today_date

    @property
    def content_type(self) -> str:
        return self._content_type

    @property
    def content_length(self) -> int:
        return self._content_length

    @property
    def body(self) -> str:
        return self._body

    @property
    def server(self) -> str:
        return self._server

    @property
    def date(self) -> datetime:
        return self._date
