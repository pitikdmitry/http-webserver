import os

from models.content_types import ContentTypes
from models.exceptions import BadFilePathException
from models.file import File
from models.request import Request

from urllib import parse
import aiofiles

from models.response_get import ResponseGet
from models.response_head import ResponseHead


class Executor:

    def __init__(self):
        self._document_root = os.getcwd() + "/http-test-suite/"

    async def execute(self, request: Request):
        if request.method not in ('GET', 'HEAD'):
            return ResponseGet(ResponseGet.OK, protocol=request.protocol)
        elif request.method == "HEAD":
            return self.execute_head(request)
        else:
            return await self.execute_get(request)

    def execute_head(self, request: Request) -> ResponseHead:
        try:
            file = self.get_file_info(request)
        except BadFilePathException:
            return ResponseHead(status_code=ResponseHead.FORBIDDEN, protocol=request.protocol)
        # try:
        #     content_length = self._build_content_length(resource=resource)
        # except NotFoundError:
        #     return Response(status_code=StatusCodes.NOT_FOUND, protocol=request.protocol)
        #
        # return Response(status_code=StatusCodes.OK, protocol=request.protocol,
        #                 content_length=content_length, content_type=resource.content_type.value, body=b'')

    async def execute_get(self, request: Request) -> ResponseGet:
        try:
            file = self.get_file_info(request)
        except BadFilePathException:
            return ResponseGet(status_code=ResponseGet.FORBIDDEN, protocol=request.protocol)

        try:
            body = await self.read_file(file.file_path)
        except FileNotFoundError:
            if request.url[-1:] == '/':
                return ResponseGet(status_code=ResponseGet.FORBIDDEN, protocol=request.protocol)
            else:
                return ResponseGet(status_code=ResponseGet.NOT_FOUND, protocol=request.protocol)
        except NotADirectoryError:
            return ResponseGet(status_code=ResponseGet.NOT_FOUND, protocol=request.protocol)

        return ResponseGet(status_code=ResponseGet.OK,
                           protocol=request.protocol,
                           content_type=file.content_type.value,
                           content_length=len(body),
                           body=body)

    def get_file_info(self, request: Request) -> File:

        file_path = self.check_last_slash(request.url)
        self.check_dots(file_path)
        file_path = self.try_decode(file_path)

        full_file_path = os.path.join(self._document_root, file_path)
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
            return ContentTypes["html"]

    @staticmethod
    async def read_file(filename: str) -> bytes:
        if not os.path.isfile(filename):
            raise FileNotFoundError

        async with aiofiles.open(filename, mode='rb') as f:
            return await f.read()
