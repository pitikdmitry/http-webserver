from datetime import datetime


class ResponseHead:
    # status-codes
    OK = '200 OK'
    NOT_FOUND = '404 Not Found'
    METHOD_NOT_ALLOWED = '405 Method Not Allowed'
    FORBIDDEN = '403 Forbidden'
    #

    today_date = datetime.today()

    def __init__(self,
                 status_code: str,
                 protocol: str,
                 connection=None):
        self._status_code = status_code
        self._protocol = protocol
        self._server = "server"
        self._date = ResponseHead.today_date
        self._connection = connection

    @property
    def status_code(self) -> str:
        return self._status_code

    @property
    def protocol(self) -> str:
        return self._protocol

    @property
    def server(self) -> str:
        return self._server

    @property
    def date(self) -> datetime:
        return self._date

    @property
    def connection(self) -> str:
        return self._connection
