

class File:

    def __init__(self, file_path=None, content_type=None):
        self._file_path = file_path
        self._content_type = content_type

    @property
    def file_path(self):
        return self._file_path

    @property
    def content_type(self):
        return self._content_type
