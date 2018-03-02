from models.request import Request


class Parser:

    def __init__(self):
        pass

    def get_values(self, data) -> Request:
        arr = data.split("\r\n")
        method, query, protocol = self.method_query_protocol(arr[0])
        url = self.url(query)
        return Request(method, protocol, url)

    @staticmethod
    def method_query_protocol(str_m_q_r: str) -> tuple:
        list_m_q_r = str_m_q_r.split()
        method = list_m_q_r[0]
        query = list_m_q_r[1]
        protocol = list_m_q_r[2]
        return method, query, protocol

    @staticmethod
    def url(query: str) -> str:
        list_q_p = query.split("?")
        return list_q_p[0]
