import os

import logging


class Config:

    def __init__(self, file_name):
        self._file_name = file_name
        self._cpu_limit = 4
        self._thread_limit = 256
        self._document_root = "/var/www/html"

        self._host = "0.0.0.0"
        self._port = 80
        self._log = logging.getLogger("config")
        self.read_file()

    def read_file(self):
        if not os.path.isfile(self._file_name):
            # local
            self._file_name = "./local.conf"
            # docker
            # self._file_name = "./httpd.conf"
            self._log.debug("default_config")
        else:
            self._log.debug("normal config")

        with open(self._file_name, 'r') as file:
            for line in file:
                arr = line.split()
                if arr[0] == "listen":
                    self._port = arr[1]
                elif arr[0] == "cpu_limit":
                    self._cpu_limit = arr[1]
                elif arr[0] == "thread_limit":
                    self._thread_limit = arr[1]
                elif arr[0] == "document_root":
                    self._document_root = arr[1]
                elif arr[0] == "host":
                    self._host = arr[1]
                else:
                    pass

    @property
    def file_name(self):
        return self._file_name

    @property
    def cpu_limit(self):
        return self._cpu_limit

    @property
    def thread_limit(self):
        return self._thread_limit

    @property
    def document_root(self):
        return self._document_root

    @property
    def host(self):
        return self._host

    @property
    def port(self):
        return self._port
