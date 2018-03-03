import asyncio
import logging
from Handler.handler import Handler


class Server:
    def __init__(self, address: str, port: int, handler: Handler):
        self._address = address
        self._port = port
        self._handler = handler
        self._log = logging.getLogger("server")

    def start(self):
        event_loop = asyncio.get_event_loop()
        server_gen = asyncio.start_server(self._handler.handle, self._address, self._port)
        server = event_loop.run_until_complete(server_gen)
        self._log.debug('starting up on {} port {}'.format(self._address, self._port))
        try:
            event_loop.run_forever()
        except KeyboardInterrupt:
            pass
        finally:
            self._log.debug('closing server')
            server.close()
            event_loop.run_until_complete(server.wait_closed())
            self._log.debug('closing event loop')
            event_loop.close()
