import os

from models.content_types import ContentTypes
from models.file import File
from models.request import Request
from models.response import Response


class ForbiddenError(BaseException):
    pass


class NotFoundError(BaseException):
    pass


class Executor:

    def __init__(self):
        pass

    def execute(self, request: Request):
        if request.method not in ('GET', 'HEAD'):
            return Response(Response.OK, protocol=request.protocol)
        elif request.method == "HEAD":
            self.execute_head(request)
        else:
            self.execute_get(request)

    def execute_head(self, request: Request):
        self._build_resource(request)

    def execute_get(self, request: Request):
        self._build_resource(request)

    def _build_resource(self, request: Request) -> File:

        url = self.check_last_slash(request.url)
        self.check_dots(url)

        working_dir = os.getcwd()
        print(working_dir)
        file_path = os.path.join(working_dir + "/tests/static", url)
        content_type = self.get_content_type(file_path)

        # return File(path=filename, file_path=file_path, content_type=content_type)
        return File()

    @staticmethod
    def check_last_slash(url: str) -> str:
        if url[-1:] == '/':
            return url[1:] + 'index.html'
        else:
            return url[1:]

    @staticmethod
    def check_dots(url: str) -> None:
        if len(url.split('../')) > 1:
            raise ForbiddenError

    @staticmethod
    def get_content_type(file_path) -> str:
        try:
            content_type = file_path.split('.')[-1]
            return ContentTypes[content_type]
        except KeyError:
            return ContentTypes["plain"]
