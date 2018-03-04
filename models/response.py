from datetime import datetime


class Response:
    # status-codes
    OK = '200 OK'
    NOT_FOUND = '404 Not Found'
    METHOD_NOT_ALLOWED = '405 Method Not Allowed'
    FORBIDDEN = '403 Forbidden'
    #

    def __init__(self, status_code,
                 protocol,
                 connection,
                 content_type='',
                 content_length=0,
                 body=b''):
        self._status_code = status_code
        self._protocol = protocol
        self._connection = connection
        self._content_type = content_type
        self._content_length = content_length
        self._body = body

        self._server = "server"
        self._date = Response.today_date

    today_date = datetime.today()

    @property
    def status_code(self):
        return self._status_code

    @property
    def protocol(self):
        return self._protocol

    @property
    def connection(self):
        return self._connection

    @property
    def content_type(self):
        return self._content_type

    @property
    def content_length(self):
        return self._content_length

    @property
    def body(self):
        return self._body

    @property
    def server(self):
        return self._server

    @property
    def date(self):
        return self._date
