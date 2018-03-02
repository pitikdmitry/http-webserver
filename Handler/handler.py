import logging


class Handler:
    def __init__(self):
        pass

    async def handle_hello(self, reader, writer):
        address = writer.get_extra_info('peername')
        log = logging.getLogger('echo_{}_{}'.format(*address))
        log.debug('connection accepted')

        block_size = 128
        data = b""
        while True:
            block = await reader.read(block_size)
            data += block

            if not block:
                break

        if len(data) > 0:
            self.parse(data.decode())
            log.debug('received {!r}'.format(data))
            writer.write(data)
            await writer.drain()
            log.debug('sent {!r}'.format(data))
        else:
            log.debug('closing')
            writer.close()
            return

    def parse(self, data: str):
        for line in data:
            print(line)

