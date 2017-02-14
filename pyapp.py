import pymongo
import uuid
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options
from tornado.web import url

from handlers.handlers import *


define("port", default=8089, type=int)
define("config_file", default="app_config.yml", help="app_config file")

MONGO_SERVER = 'localhost'


class Application(tornado.web.Application):
    def __init__(self, **overrides):
        handlers = [
        url(r'/',MainHandler, name='first')
        url(r'/', HelloHandler, name='index'),
        url(r'/hello', HelloHandler, name='hello'),
        url(r'/email', EmailMeHandler, name='email'),
        url(r'/message', GmessageHandler, name='gmessage'),
        url(r'/gmessage', MessageHandler, name='message'),
        url(r'/grav', GravatarHandler, name='grav'),
        url(r'/menu', MenuTagsHandler, name='menu'),
        url(r'/slidy', SlidyHandler, name='slidy'),
        url(r'/notification', NotificationHandler, name='notification'),
        url(r'/popup', PopupHandler, name='popup_demo'),
        url(r'/tail', TailHandler, name='tail_demo'),
        url(r'/pusher', DataPusherHandler, name='push_demo'),
        url(r'/pusher_raw', DataPusherRawHandler, name='push_raw_demo'),
        url(r'/back_to_where_you_came_from', ReferBackHandler, name='referrer'),
        url(r'/thread', ThreadHandler, name='thread_handler'),
        url(r'/login_no_block', NoneBlockingLogin, name='login_no_block'),
        url(r'/login', LoginHandler, name='login'),
        url(r'/register', RegisterHandler, name='register'),
        url(r'/logout', LogoutHandler, name='logout'),

        ]


        settings = {
            'static_path': os.path.join(os.path.dirname(__file__), 'static'),
            'template_path': os.path.join(os.path.dirname(__file__), 'templates'),
            "cookie_secret":    base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes),
            'mandrill_key': 'KEY',
            'mandrill_url': 'https://mandrillapp.com/api/1.0/',

            'xsrf_cookies': False,
            'debug': True,
            'log_file_prefix': "tornado.log",
        }

        tornado.web.Application.__init__(self, handlers, **settings)

        self.syncconnection = pymongo.MongoClient(MONGO_SERVER, 27017)

        if 'db' in overrides:
            self.syncdb = self.syncconnection[overrides['db']]
        else:
            self.syncdb = self.syncconnection["test-thank"]

        #self.syncconnection.close()



def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()
