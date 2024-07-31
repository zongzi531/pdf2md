import tornado
from tornado.options import define, options
from handers import Pdf2Md

define("port", default=3000, help="run on the given port", type=int)

application = tornado.web.Application([
  (r"/p2m", Pdf2Md),
])

print("Running on http://localhost:{}".format(options.port))

application.listen(options.port)
tornado.ioloop.IOLoop.instance().start()
