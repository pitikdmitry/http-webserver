import os

from models.content_types import ContentTypes
from models.file import File
from models.request import Request
from models.response import Response

import aiofiles


class ForbiddenError(BaseException):
    pass


class NotFoundError(BaseException):
    pass


class Executor: #   добавить async методы сюда везде

    def __init__(self):
        pass

    def execute(self, request: Request) -> Response:
        if request.method not in ('GET', 'HEAD'):
            return Response(Response.OK, protocol=request.protocol)
        elif request.method == "HEAD":
            return self.execute_head(request)
        else:
            return self.execute_get(request)

    def execute_head(self, request: Request) -> Response:
        try:
            file = self.get_file(request)
        except ForbiddenError:
            return Response(status_code=Response.FORBIDDEN, protocol=request.protocol)
        # try:
        #     content_length = self._build_content_length(resource=resource)
        # except NotFoundError:
        #     return Response(status_code=StatusCodes.NOT_FOUND, protocol=request.protocol)
        #
        # return Response(status_code=StatusCodes.OK, protocol=request.protocol,
        #                 content_length=content_length, content_type=resource.content_type.value, body=b'')

    def execute_get(self, request: Request):
        try:
            file = self.get_file(request)
        except ForbiddenError:
            return Response(status_code=Response.FORBIDDEN, protocol=request.protocol)

        try:
            body = self.read_file(file.file_path)
        except FileNotFoundError:
            if request.url[-1:] == '/':
                return Response(status_code=Response.FORBIDDEN, protocol=request.protocol)
            else:
                return Response(status_code=Response.NOT_FOUND, protocol=request.protocol)
        except NotADirectoryError:
            return Response(status_code=Response.NOT_FOUND, protocol=request.protocol)

        return Response(status_code=Response.OK,
                        protocol=request.protocol,
                        content_type=file.content_type.value,
                        content_length=len(body),
                        body=body)

    def get_file(self, request: Request) -> File:

        file_path = self.check_last_slash(request.url)
        self.check_dots(file_path)

        working_dir = os.getcwd()
        full_file_path = os.path.join(working_dir + "/tests/static", file_path)
        content_type = self.get_content_type(file_path)

        return File(full_file_path, content_type)

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
    def get_content_type(file_path) -> ContentTypes:
        try:
            content_type_name = file_path.split('.')[-1]
            return ContentTypes[content_type_name]
        except KeyError:
            return ContentTypes["plain"]

    @staticmethod
    def read_file(filename: str) -> bytes:
        with aiofiles.open(filename, mode='rb') as f:
            return f.read()
