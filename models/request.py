class Request:

    def __init__(self, method, protocol, url, connection):
        self._method = method
        self._protocol = protocol
        self._url = url
        self._connection = connection

    @property
    def method(self):
        return self._method

    @property
    def protocol(self):
        return self._protocol

    @property
    def url(self):
        return self._url

    @property
    def connection(self):
        return self._connection
