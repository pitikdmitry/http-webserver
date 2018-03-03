import logging

from Handler.executor import Executor
from Handler.parser import Parser
from Handler.serializer import Serializer


class Handler:
    def __init__(self):
        self._parser = Parser()
        self._executor = Executor()
        self._serializer = Serializer()

    async def handle(self, reader, writer):
        address = writer.get_extra_info('peername')
        log = logging.getLogger('echo_{}_{}'.format(*address))
        log.debug('connection accepted')

        block_size = 128
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
            log.debug('received {!r}'.format(data))

            request = self._parser.get_values(data.decode())
            response = await self._executor.execute(request)
            response_data = self._serializer.dump(response)

            writer.write(response_data)
            await writer.drain()
            writer.close()
            log.debug('sent {!r}'.format(response_data))
        else:
            log.debug('closing')
            writer.close()
            return
