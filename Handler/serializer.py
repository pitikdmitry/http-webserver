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
        return f"HTTP/{response.protocol} {response.status_code}\r\n" \
               f"Server: Server\r\n" \
               f"Content-Type: {response.content_type}\r\n" \
               f"Content-Length: {response.content_length}\r\n\r\n"

    @staticmethod
    def _error_response(response: Response) -> str:
        return f"HTTP/{response.protocol} {response.status_code}\r\n" \
               f"Server: Server\r\n\r\n"
