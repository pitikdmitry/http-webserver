from models.request import Request


class Parser:

    def __init__(self):
        pass

    def get_values(self, data) -> Request:
        arr = data.split("\r\n")
        method, query, protocol = self.method_query_protocol(arr[0])
        url, query_params = self.url_params(query)
        headers = self.headers(arr)
        return Request(method, protocol, url, headers, query_params)

    @staticmethod
    def method_query_protocol(str_m_q_r: str) -> tuple:
        list_m_q_r = str_m_q_r.split()
        method = list_m_q_r[0]
        query = list_m_q_r[1]
        protocol = list_m_q_r[2]
        return method, query, protocol

    @staticmethod
    def headers(arr) -> {}:
        headers = {}
        for i in range(1, len(arr)):
            if arr[i] == "":
                continue
            header_list = arr[i].split()
            h_type = header_list[0]
            h_val = header_list[1]
            headers[h_type] = h_val
        return headers

    @staticmethod
    def url_params(query: str) -> tuple:
        list_q_p = query.split("?")
        url = list_q_p[0]
        params = {}
        if list_q_p[1]:
            params_list = list_q_p[1].split("&")
            for i in range(0, len(params_list)):
                list_param_val = params_list[i].split("=")
                param = list_param_val[0]
                val = list_param_val[1]
                params[param] = val

        return url, params


