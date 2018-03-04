from models.response import Response


class Serializer:

    def __init__(self):
        pass

    @staticmethod
    def dump(response):
        if response.status_code == Response.OK:
            return Serializer.good_response(response).encode() + response.body
        else:
            return Serializer.bad_response(response).encode()

    @staticmethod
    def good_response(response):
        return "{} {}\r\n" \
               "Server: {}\r\n" \
               "Date: {}\r\n" \
               "Connection: {}\r\n" \
               "Content-Length: {}\r\n" \
               "Content-Type: {}\r\n\r\n".format(response.protocol, response.status_code,
                                                 response.server, response.date, response.connection,
                                                 response.content_length, response.content_type)

    @staticmethod
    def bad_response(response):
        return "{} {}\r\n" \
               "Server: {}\r\n" \
               "Date: {}\r\n" \
               "Connection: {}\r\n\r\n".format(response.protocol, response.status_code,
                                               response.server, response.date, response.connection)
