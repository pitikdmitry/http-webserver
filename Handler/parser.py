from models.request import Request
import logging


class Parser:

    def __init__(self):
        self._log = logging.getLogger("parser")

    def get_values(self, data):
        try:
            arr = data.split("\r\n")
            method, query, protocol = self.method_query_protocol(arr[0])
            url = self.url(query)
            connection = self.get_connection()

        except BaseException as e:
            self._log.debug('parsing exc: {}'.format(e))
            return Request("unknown", "unknown", "unknown", "unknown")
        return Request(method, protocol, url, connection)

    @staticmethod
    def method_query_protocol(str_m_q_r):
        list_m_q_r = str_m_q_r.split()
        method = list_m_q_r[0]
        query = list_m_q_r[1]
        protocol = list_m_q_r[2]
        return method, query, protocol

    @staticmethod
    def url(query):
        list_q_p = query.split("?")
        return list_q_p[0]

    @staticmethod
    def get_connection():
        return ''
