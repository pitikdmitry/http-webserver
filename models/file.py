class File:

    def __init__(self, file_path: str = None, content_type: str = None) -> None:
        self._file_path = file_path
        self._content_type = content_type

    @property
    def file_path(self) -> str:
        return self._file_path

    @property
    def content_type(self) -> str:
        return self._content_type
