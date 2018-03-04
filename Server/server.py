import asyncio
import logging

import os
import uvloop


class Server:
    def __init__(self, address, port, config, handler):
        self._address = address
        self._port = port
        self._config = config
        self._handler = handler
        self._log = logging.getLogger("server")

        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    def start(self):
        forks = []
        for i in range(0, int(self._config.cpu_limit) * 2):
            pid = os.fork()
            forks.append(pid)
            if pid == 0:
                event_loop = asyncio.get_event_loop()
                self._log.debug("pid: ", os.getpid())

                # for i in range(0, int(self._config.thread_limit)):
                server_gen = asyncio.start_server(self._handler.handle, self._address, self._port, reuse_port=True)
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

    def start_one(self):
        event_loop = asyncio.get_event_loop()
        server_gen = asyncio.start_server(self._handler.handle, self._address, self._port, reuse_port=True)
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
