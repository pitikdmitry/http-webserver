import os

from models.content_types import ContentTypes
from models.exceptions import FileNotFoundException, BadFilePathException
from models.file import File
from models.request import Request
from models.response import Response

from urllib import parse
import aiofiles


class Executor:

    def __init__(self):
        pass

    async def execute(self, request: Request) -> Response:
        if request.method not in ('GET', 'HEAD'):
            return Response(Response.OK, protocol=request.protocol)
        elif request.method == "HEAD":
            return self.execute_head(request)
        else:
            return await self.execute_get(request)

    def execute_head(self, request: Request) -> Response:
        try:
            file = self.get_file_info(request)
        except BadFilePathException:
            return Response(status_code=Response.FORBIDDEN, protocol=request.protocol)
        # try:
        #     content_length = self._build_content_length(resource=resource)
        # except NotFoundError:
        #     return Response(status_code=StatusCodes.NOT_FOUND, protocol=request.protocol)
        #
        # return Response(status_code=StatusCodes.OK, protocol=request.protocol,
        #                 content_length=content_length, content_type=resource.content_type.value, body=b'')

    async def execute_get(self, request: Request) -> Response:
        try:
            file = self.get_file_info(request)
        except BadFilePathException:
            return Response(status_code=Response.FORBIDDEN, protocol=request.protocol)

        try:
            body = await self.read_file(file.file_path)
        except FileNotFoundError:
            if request.url[-1:] == '/':
                return Response(status_code=Response.FORBIDDEN, protocol=request.protocol)
            else:
                return Response(status_code=Response.NOT_FOUND, protocol=request.protocol)
        except NotADirectoryError:
            return Response(status_code=Response.NOT_FOUND, protocol=request.protocol)

        resp = Response(status_code=Response.OK,
                        protocol=request.protocol,
                        content_type=file.content_type.value,
                        content_length=len(body),
                        body=body)
        return resp

    def get_file_info(self, request: Request) -> File:

        file_path = self.check_last_slash(request.url)
        self.check_dots(file_path)
        file_path = self.try_decode(file_path)

        working_dir = os.getcwd()
        full_file_path = os.path.join(working_dir + "/http-test-suite/", file_path)
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
        if url.find("../") != -1:
            raise BadFilePathException

    @staticmethod
    def try_decode(url):
        url = parse.unquote(url)
        return url

    @staticmethod
    def get_content_type(file_path) -> ContentTypes:
        try:
            content_type_name = file_path.split('.')[-1]
            return ContentTypes[content_type_name]
        except KeyError:
            return ContentTypes["plain"]

    @staticmethod
    async def read_file(filename: str) -> bytes:
        if not os.path.isfile(filename):
            raise FileNotFoundException

        async with aiofiles.open(filename, mode='rb') as f:
            return await f.read()
