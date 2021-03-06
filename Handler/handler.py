import logging

from Handler.executor import Executor
from Handler.parser import Parser
from Handler.serializer import Serializer


class Handler:
    def __init__(self):
        self._parser = Parser()
        self._executor = Executor()
        self._serializer = Serializer()
        self._log = logging.getLogger("handler")

    async def handle(self, reader, writer):
        address = writer.get_extra_info('peername')
        self._log.debug('echo_{}_{}'.format(*address))
        self._log.debug('connection accepted')

        block_size = 1024
        data = b""
        while True:
            block = await reader.read(block_size)
            data += block

            if not block or reader.at_eof():
                break

            if data[-4:] == b'\r\n\r\n':
                break

        if len(data) > 0:
            self._log.debug('received {!r}'.format(data))

            request = self._parser.get_values(data.decode())
            response = await self._executor.execute(request)
            response_data = self._serializer.dump(response)

            writer.write(response_data)
            await writer.drain()
            writer.close()
            # self._log.debug('sent {!r}'.format(response_data))
        else:
            self._log.debug('closing')
            writer.close()
            return
