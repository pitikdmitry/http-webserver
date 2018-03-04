class Config:

    def __init__(self, file_name):
        self._file_name = file_name
        self._listen = 80
        self._cpu_limit = 4
        self._thread_limit = 256
        self._document_root = "/var/www/html"

        self._host = "127.0.0.1"
        self._port = 80
        self.read_file()

    def read_file(self):
        with open(self._file_name, 'r') as file:
            for line in file:
                arr = line.split()
                if arr[0] == "listen":
                    self._listen = arr[1]
                elif arr[0] == "cpu_limit":
                    self._cpu_limit = arr[1]
                elif arr[0] == "thread_limit":
                    self._thread_limit = arr[1]
                elif arr[0] == "document_root":
                    self._document_root = arr[1]
                else:
                    pass

    @property
    def file_name(self):
        return self._file_name

    @property
    def listen(self):
        return self._listen

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
