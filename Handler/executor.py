from models.request import Request


class Executor:

    def __init__(self):
        pass

    def execute(self, request: Request):
        if request.method not in ('GET', 'HEAD'):

        elif request.method == "HEAD":
            self.execute_head()
        else:
            self.execute_get()

    def execute_head(self):
        pass

    def execute_get(self):
        pass
