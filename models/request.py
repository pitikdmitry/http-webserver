class Request:

    def __init__(self, method: str, protocol: str, url: str, connection: str) -> None:
        self._method = method
        self._protocol = protocol
        self._url = url
        self._connection = connection

    @property
    def method(self) -> str:
        return self._method

    @property
    def protocol(self) -> str:
        return self._protocol

    @property
    def url(self) -> str:
        return self._url

    @property
    def connection(self) -> str:
        return self._connection
