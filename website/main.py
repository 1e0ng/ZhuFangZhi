#encoding:utf-8
#Created by Liang Sun in 2012 

import tornado.ioloop
from tornado.options import define, options, logging
import tornado.web

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
    def get(self, query_string):
        self.write("You queried: " + query_string)


def main():
    tornado.options.parse_command_line()
    logging.info("Starting Tornado web server on http://localhost:%s" % options.port)
    application = tornado.web.Application([
        (r"/", MainHandler),
	(r"/search/(.*)", SearchHandler),
    ], **settings)
    application.listen(options.port, **server_settings)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
