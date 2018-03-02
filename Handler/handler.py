import logging

from Handler.executor import Executor
from Handler.parser import Parser


class Handler:
    def __init__(self):
        self._parser = Parser()
        self._executor = Executor()

    async def handle(self, reader, writer):
        address = writer.get_extra_info('peername')
        log = logging.getLogger('echo_{}_{}'.format(*address))
        log.debug('connection accepted')

        block_size = 8
        data = b""
        while True:
            block = await reader.read(block_size)
            data += block

            if not block or reader.at_eof():
                break

            print(data[-4:])
            if data[-4:] == b'\r\n\r\n':
                break

        if len(data) > 0:
            request = self._parser.get_values(data.decode())
            self._executor.execute_request(request)
            log.debug('received {!r}'.format(data))
            writer.write(data)
            await writer.drain()
            log.debug('sent {!r}'.format(data))
        else:
            log.debug('closing')
            writer.close()
            return





