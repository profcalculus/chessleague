from flask_restful import reqparse

class BaseRequestParser(reqparse.RequestParser):
    def __init__(self, *args, **kwargs):
        kwargs['bundle_errors'] = True
        super(BaseRequestParser, self).__init__(*args, **kwargs)
        # self.add_argument('id', type=int)
