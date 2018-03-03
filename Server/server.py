import asyncio
import logging
from Handler.handler import Handler


class Server:
    def __init__(self, address: str, port: int, handler: Handler):
        self._address = address
        self._port = port
        self._handler = handler

    # def start(self):
    #
    #     event_loop = asyncio.get_event_loop()
    #     task = asyncio.start_server(self._handler.handle, host=self._address, port=self._port)
    #     event_loop.create_task(task)
    #     logging.debug('starting up on {} port {}'.format(self._address, self._port))
    #
    #     try:
    #         event_loop.run_forever()
    #     except KeyboardInterrupt:
    #         pass
    #     finally:
    #         logging.debug('closing server')
    #         # task.close()
    #         # event_loop.run_until_complete(task.wait_closed())
    #         logging.debug('closing event loop')
    #         # event_loop.close()
    def start(self):
        event_loop = asyncio.get_event_loop()
        factory = event_loop.create_server(self._handler.handle, host=self._address)
        server = event_loop.run_until_complete(factory)
        logging.debug('starting up on {} port {}'.format(self._address, self._port))
        try:
            event_loop.run_forever()
        except KeyboardInterrupt:
            pass
        finally:
            logging.debug('closing server')
            server.close()
            event_loop.run_until_complete(server.wait_closed())
            logging.debug('closing event loop')
            event_loop.close()
