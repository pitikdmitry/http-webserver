from models.response import Response


class Serializer:

    @staticmethod
    def dump(response: Response) -> bytes:
        if response.status_code == Response.OK:
            return Serializer.good_response(response).encode() + response.body
        else:
            return Serializer.bad_response(response).encode()

    @staticmethod
    def good_response(response: Response) -> str:
        return "{} {}\r\n" \
               "Server: Server\r\n" \
               "Content-Type: {}\r\n" \
               "Content-Length: {}\r\n\r\n".format(response.protocol, response.status_code,
                                                   response.content_type, response.content_length)

    @staticmethod
    def bad_response(response: Response) -> str:
        return "{} {}\r\n" \
               "Server: Server\r\n\r\n".format(response.protocol, response.status_code)
