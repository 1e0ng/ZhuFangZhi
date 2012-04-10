#encoding:utf-8
#Created by Liang Sun in 2012 

import tornado.ioloop
from tornado.options import define, options, logging
import tornado.web
import tornado.database

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
        items = [{"title":"上海租房网,上海租房信息,上海租房信息, 租房子,搜屋网。",
            "url":"http://www.url.com",
            "price":"823元/月",
            "area":"80平米",
            "style":"2室1厅1卫",
            "address":"海淀区学院南路东三元胡同",
            "district":"屯三里小区"}] * 10
        self.render("search.html", query=self.get_argument("query"), items=items)
        #self.write("Your query is " + self.get_argument("query"))
        
def main():
    tornado.options.parse_command_line()
    logging.info("Starting Tornado web server on http://localhost:%s" % options.port)
    application = tornado.web.Application([
        (r"/", MainHandler),
        (r"/search", SearchHandler),
    ], **settings)
    application.listen(options.port, **server_settings)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
