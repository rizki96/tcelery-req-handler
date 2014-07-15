__author__ = 'rizki'

import logging
import tornado.auth
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.escape

from tornado import gen
from tornado.web import asynchronous

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('main')

class InitHandler(tornado.web.RequestHandler):
    def get(self):
        from backend import model
        '''
        user = model.User(name='user1', password='test', photo=None, is_superadmin=False, is_active=True)
        user.save()
        user = model.User(name='user2', password='test', photo=None, is_superadmin=False, is_active=True)
        user.save()
        user = model.User(name='user3', password='test', photo=None, is_superadmin=False, is_active=True)
        user.save()
        user = model.User(name='user4', password='test', photo=None, is_superadmin=False, is_active=True)
        user.save()
        user = model.User(name='user5', password='test', photo=None, is_superadmin=False, is_active=True)
        user.save()
        user = model.User(name='user6', password='test', photo=None, is_superadmin=False, is_active=True)
        user.save()
        user = model.User(name='user7', password='test', photo=None, is_superadmin=False, is_active=True)
        user.save()
        user = model.User(name='user8', password='test', photo=None, is_superadmin=False, is_active=True)
        user.save()
        user = model.User(name='user9', password='test', photo=None, is_superadmin=False, is_active=True)
        user.save()
        user = model.User(name='user10', password='test', photo=None, is_superadmin=False, is_active=True)
        user.save()
        '''
        '''
        exists = model.User.table_exists()
        if not exists:
            model.User.create_table(True)
        exists = model.Patient.table_exists()
        if not exists:
            model.Patient.create_table_fts(content=model.Patient.summary, fail_silently=True)
        exists = model.Doctor.table_exists()
        if not exists:
            model.Doctor.create_table_fts(content=model.Doctor.summary, fail_silently=True)
        exists = model.Appointment.table_exists()
        if not exists:
            model.Appointment.create_table(True)
        '''
        self.write('InitHandler')

class AppHandler(tornado.web.RequestHandler):
    @asynchronous
    @gen.coroutine
    def get(self, *args):
        self.set_header("Content-Type", "application/json")
        kwargs = {}
        if not self.get_tasks:
            self.raise404()
        kwargs['_query'] = self.request.query_arguments
        kwargs['_body'] = self.request.body_arguments
        response = yield self.task_handler.get_one(0, *args, **kwargs)
        if response.result:
            self.write(response.result.replace('"', '').replace("'", '"'))
        else:
            self.raise404()
        self.finish()

    @asynchronous
    @gen.coroutine
    def post(self, *args):
        self.set_header("Content-Type", "application/json")
        kwargs = {}
        if not self.post_tasks:
            self.raise404()
        kwargs['_query'] = self.request.query_arguments
        kwargs['_body'] = self.request.body_arguments
        response = yield self.task_handler.post_one(0, *args, **kwargs)
        if response.result:
            self.write(response.result.replace('"', '').replace("'", '"'))
        else:
            self.raise404()
        self.finish()

    @asynchronous
    @gen.coroutine
    def put(self, *args):
        self.set_header("Content-Type", "application/json")
        kwargs = {}
        if not self.put_tasks:
            self.raise404()
        kwargs['_query'] = self.request.query_arguments
        kwargs['_body'] = self.request.body_arguments
        response = yield self.task_handler.put_one(0, *args, **kwargs)
        if response.result:
            self.write(response.result.replace('"', '').replace("'", '"'))
        else:
            self.raise404()
        self.finish()

    @asynchronous
    @gen.coroutine
    def delete(self, *args):
        self.set_header("Content-Type", "application/json")
        kwargs = {}
        if not self.delete_tasks:
            self.raise404()
        kwargs['_query'] = self.request.query_arguments
        kwargs['_body'] = self.request.body_arguments
        response = yield self.task_handler.delete_one(0, *args, **kwargs)
        if response.result:
            self.write(response.result.replace('"', '').replace("'", '"'))
        else:
            self.raise404()
        self.finish()
