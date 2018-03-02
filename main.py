from Server.server import Server
from Handler.handler import Handler
import logging
import sys

logging.basicConfig(
    level=logging.DEBUG,
    format='%(name)s: %(message)s',
    stream=sys.stderr,
)

if __name__ == '__main__':
    handler = Handler()
    server = Server("127.0.0.1", 10001, handler)
    server.start()
