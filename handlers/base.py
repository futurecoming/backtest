import re
from tornado.web import RequestHandler


class BaseHandler(RequestHandler):
    def set_default_headers(self):
        self.allowMyOrigin()

    def initialize(self):
        self.session = self.application.DB_Session()

    def on_finish(self):
        self.session.close()

    #  允许跨域访问的地址
    def allowMyOrigin(self):
        allow_list = [
            'http://127.0.0.1:7100',
        ]
        if 'Origin' in self.request.headers:
            Origin = self.request.headers['Origin']
            # 域名
            re_ret = re.match(r".{1,}\.(foo.com|bar.com)", Origin)
            # 内网和本地
            re_ret2 = re.match(r"^(192.168.1.*|127.0.0.1.*|192.168.2.*)", Origin)
            if re_ret or re_ret2 or Origin in allow_list:
                self.set_header("Access-Control-Allow-Origin", Origin)  # 这个地方可以写域名
                self.set_header("Access-Control-Allow-Headers", "x-requested-with")
                self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
