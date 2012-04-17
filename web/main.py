#encoding:utf-8
#Created by Liang Sun in 2012 

import tornado.ioloop
from tornado.options import define, options, logging
import tornado.web
from tornado.database import Connection

define("port", default=8888, help="run on the given port", type=int)

settings = {
    "debug": True,
}

server_settings = {
    "xheaders" : True,
}

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("home.html")

class SearchHandler(tornado.web.RequestHandler):
    def get(self):
        db = Connection('127.0.0.1', 'zfz', 'zfz', 'zfz...891', 25200)
        q = self.get_argument(name="query", default="")

        q = q.lstrip().rstrip().replace("'", "").replace('"', '').replace('#', '').replace('%', '')
        qs = q.split(' ')

        if len(q) > 0:
            if len(qs) == 1:
                q = '%' + q + '%'
                items = db.query("select title, url, price, area, arch, address, district "
                        "from pages where address like %s or district like %s or title like %s "
                        "order by date desc limit 20", q, q, q)
            else:
                l = qs[0]
                r = qs[-1]
                m1 = ''
                m2 = ''
                for i in range(1, len(qs) - 1):
                    m1 += '%' + qs[i]
                    m2 += '%' + qs[len(qs) - 1 - i]

                m1 += '%'
                m2 += '%'

                items = db.query("select title, url, price, area, arch, address, district "
                        "from pages where (address like %s and district like %s) or "
                        "(address like %s and district like %s) or "
                        "(title like %s and address like %s) or "
                        "(title like %s and address like %s and district like %s) or "
#                        "title like %s or "
                        "address like %s "
                        "order by date desc limit 20",
                        '%' + l + m1, '%' + r + '%',
                        '%' + r + m2, '%' + l + '%',
                        '%' + l + '%', m1 + r + '%',
                        '%' + l + '%', m1, '%' + r + '%',
#                        '%' + l + m1 + r + '%',
                        '%' + l + m1 + r + '%')
        else:
            items = []

        if len(items) < 1:
            hit = False
        else:
            hit = True

        self.render("search.html", query=self.get_argument("query", default=""), items=items, hit=hit)
        #self.write("Your query is " + self.get_argument("query"))
        
def main():
    tornado.options.parse_command_line()
    logging.info("Starting Tornado web server on http://localhost:%s" % options.port)
    application = tornado.web.Application([
        (r"/", MainHandler),
        (r"/search", SearchHandler),
        (r".*", MainHandler),
    ], **settings)
    application.listen(options.port, **server_settings)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
