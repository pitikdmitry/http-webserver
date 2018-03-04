import os
import logging

from models.config import Config
from models.content_types import ContentTypes
from models.exceptions import BadFilePathException, ForbiddenException
from models.file import File

from urllib import parse
import aiofiles

from models.response import Response


class Executor:

    def __init__(self):
        self._config = Config("/etc/httpd.conf")
        self._files_root = self._config.document_root + "/http-test/"
        logging.debug(r"doc root: " + self._config.document_root)
        # self._document_root = os.getcwd() + "/http-test/"

    async def execute(self, request):
        if request.method not in ('GET', 'HEAD'):
            return Response(Response.METHOD_NOT_ALLOWED, protocol=request.protocol, connection=request.connection)
        elif request.method == "HEAD":
            return self.execute_head(request)
        else:
            return await self.execute_get(request)

    def execute_head(self, request):
        try:
            file = self.get_file_info(request)
            content_length = self.get_file_content_length(file.file_path)
            return Response(status_code=Response.OK,
                            protocol=request.protocol,
                            connection=request.connection,
                            content_type=file.content_type.value,
                            content_length=content_length)

        except (BadFilePathException, FileNotFoundError):
            return Response(status_code=Response.NOT_FOUND, protocol=request.protocol, connection=request.connection)

    async def execute_get(self, request):
        try:
            file = self.get_file_info(request)
            body = await self.read_file(file.file_path, request.url)
            return Response(status_code=Response.OK,
                            protocol=request.protocol,
                            connection=request.connection,
                            content_type=file.content_type.value,
                            content_length=len(body),
                            body=body)
        except (BadFilePathException, FileNotFoundError):
            return Response(status_code=Response.NOT_FOUND, protocol=request.protocol, connection=request.connection)
        except ForbiddenException:
            return Response(status_code=Response.FORBIDDEN, protocol=request.protocol, connection=request.connection)

    def get_file_info(self, request):

        file_path = self.check_last_slash(request.url)
        self.check_dots(file_path)
        file_path = self.try_decode(file_path)

        full_file_path = os.path.join(self._files_root, file_path)
        logging.info("full_file_path: " + full_file_path)
        content_type = self.get_content_type(file_path)

        return File(full_file_path, content_type)

    @staticmethod
    def check_last_slash(url):
        if url[-1:] == '/':
            return url[1:] + 'index.html'
        else:
            return url[1:]

    @staticmethod
    def check_dots(url):
        if url.find("../") != -1:
            raise BadFilePathException

    @staticmethod
    def try_decode(url):
        url = parse.unquote(url)
        return url

    @staticmethod
    def get_content_type(file_path):
        try:
            content_type_name = file_path.split('.')[-1]
            return ContentTypes[content_type_name]
        except KeyError:
            return ContentTypes["html"]

    @staticmethod
    async def read_file(filename, url):
        if not os.path.isfile(filename):
            if url[-1] == '/' and url.count(".") < 1:
                raise ForbiddenException
            else:
                raise FileNotFoundError

        async with aiofiles.open(filename, mode='rb') as f:
            return await f.read()

    @staticmethod
    def get_file_content_length(filename):
        if not os.path.isfile(filename):
            raise FileNotFoundError

        return os.path.getsize(filename)
