class Request:

    def __init__(self, method: str, protocol: str, url: str) -> None:
        self._method = method
        self._protocol = protocol
        self._url = url

    @property
    def method(self) -> str:
        return self._method

    @property
    def protocol(self) -> str:
        return self._protocol

    @property
    def url(self) -> str:
        return self._url
