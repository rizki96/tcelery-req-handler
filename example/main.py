__author__ = 'rizki'

import os
import tornado.auth
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import logging
import tcelery

from tornado.web import asynchronous
from tornado.options import define, options

from tcelery_req_handler import routes, tcelery_routes, tcelery_async_routes

import handler
import config
import backend.v1

tcelery.setup_nonblocking_producer()

api_version = "v1"

class Application(tornado.web.Application):
    def __init__(self):

        handlers = [
            tcelery_routes(r"/%s/user/?" % api_version,
                           get_tasks=[backend.v1.list_create_users],
                           post_tasks=[backend.v1.list_create_users],
                           handler=handler.AppHandler),
            tcelery_routes(r"/%s/user/([0-9a-fA-F]{1,})" % api_version,
                           get_tasks=[backend.v1.show_edit_delete_users],
                           put_tasks=[backend.v1.show_edit_delete_users],
                           delete_tasks=[backend.v1.show_edit_delete_users],
                           handler=handler.AppHandler),
            tcelery_async_routes(r"/%s/async_user/?" % api_version,
                                 get_tasks=[backend.v1.list_create_users]),
            tcelery_async_routes(r"/%s/async_user/([0-9a-fA-F]{1,})" % api_version,
                                 get_tasks=[backend.v1.show_edit_delete_users],
                                 put_tasks=[backend.v1.show_edit_delete_users],
                                 delete_tasks=[backend.v1.show_edit_delete_users]),
            #(r"/init", handler.InitHandler),
            (r"/", handler.MainHandler),
        ]
        settings = dict(
            title=u"Tornado Celery Handler",
            #template_path=os.path.join(os.path.dirname(__file__), "templates"),
            #static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=False,
            cookie_secret=config.default.cookie_secret,
            debug=config.default.debug,
            autoescape=None,
        )
        if settings['debug']:
            logging.getLogger().setLevel(logging.DEBUG)
        else:
            logging.getLogger().setLevel(logging.INFO)
            logging.getLogger().setLevel(logging.WARNING)

        '''
        from playhouse import apsw_ext
        from backend import model
        model.sqlitedb.initialize(apsw_ext.APSWDatabase(config.default.lite_db))
        '''

        tornado.web.Application.__init__(self, routes(handlers), **settings)

def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(config.default.server_port, config.default.server_ipaddr)
    print "Server running in port %s:%d" % (config.default.server_ipaddr, config.default.server_port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
