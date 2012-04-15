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
        db = Connection('127.0.0.1', 'zfz', 'zfz', 'zfz...891')
        q = self.get_argument(name="query", default="")

        q = q.lstrip().rstrip().replace("'", "").replace('"', '').replace('#', '').replace('%', '')
        if len(q) > 0:
            q = '%' + q + '%'
            items = db.query("select title, url, price, area, arch, address, district from pages where address like %s or district like %s limit 20", q, q)
        else:
            items = []

        if len(items) < 1:
            hit = False
        else:
            hit = True

#        items = [{"title":"上海租房网,上海租房信息,上海租房信息, 租房子,搜屋网。",
#            "url":"http://www.url.com",
#            "price":"823元/月",
#            "area":"80平米",
#            "style":"2室1厅1卫",
#            "address":"海淀区学院南路东三元胡同",
#            "district":"屯三里小区"}] * 10
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
