class Request:

    def __init__(self, method: str, protocol: str, url: str, headers: {}, params: {}) -> None:
        self._method = method
        self._protocol = protocol
        self._url = url
        self._headers = headers
        self._params = params

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
    def headers(self) -> {}:
        return self._headers

    @property
    def params(self) -> {}:
        return self._params
