from models.response import Response


class Serializer:

    @staticmethod
    def dump(response: Response) -> bytes:
        if response.status_code == Response.OK:
            return Serializer._success_response(response).encode() + response.body
        else:
            return Serializer._error_response(response).encode()

    @staticmethod
    def _success_response(response: Response) -> str:
        return "HTTP/{} {}\r\n" \
               "Server: Server\r\n" \
               "Content-Type: {}\r\n" \
               "Content-Length: {}\r\n\r\n".format(response.protocol, response.status_code,
                                                   response.content_type, response.content_length)

    @staticmethod
    def _error_response(response: Response) -> str:
        return "HTTP/{} {}\r\n" \
               "Server: Server\r\n\r\n".format(response.protocol, response.status_code)
