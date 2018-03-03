import asyncio


async def tcp_echo_client(message, loop):
    reader, writer = await asyncio.open_connection('127.0.0.1', 10001,
                                                   loop=loop)

    print('Send: %r' % message)
    writer.write(message.encode())

    data = await reader.read(100)
    print('Received: %r' % data.decode())

    print('Close the socket')
    writer.close()


message = 'GET / HTTP/1.1\r\ncache-control: no-cache\r\nPostman-Token: bee206a2-d312-4050-b2e6-21d292e96c5a\r\nUser-Agent: PostmanRuntime/7.1.1\r\nAccept: */*\r\nHost: 127.0.0.1:10001\r\naccept-encoding: gzip, deflate\r\nConnection: keep-alive\r\n\r\n'

loop = asyncio.get_event_loop()
loop.run_until_complete(tcp_echo_client(message, loop))
loop.close()
