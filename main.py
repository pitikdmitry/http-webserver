from Server.server import Server
from Handler.handler import Handler
import logging
import sys

from models.config import Config

logging.basicConfig(
    level=logging.ERROR,
    format='%(name)s: %(message)s',
    stream=sys.stderr,
)

if __name__ == '__main__':
    config = Config("/etc/httpd.conf")
    handler = Handler()
    server = Server(config.host, config.port, config, handler)
    server.start()
