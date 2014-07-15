__author__ = 'rizki'

import logging
import tornado.web

from tornado import gen
from tornado.web import asynchronous

import ptask_req_handler

class TCeleryReqHandler(tornado.web.RequestHandler, ptask_req_handler.TaskRequestHandler):

    @asynchronous
    @gen.coroutine
    def get(self, *args):
        if not self.get_tasks:
            self.raise404()
        response = yield self.task_handler.get_one(0, *args, **self.get_request_data())
        self.write(str(response.result))
        self.finish()

    @asynchronous
    @gen.coroutine
    def post(self, *args):
        if not self.post_tasks:
            self.raise404()
        response = yield self.task_handler.post_one(0, *args, **self.get_request_data())
        self.write(str(response.result))
        self.finish()

    @asynchronous
    @gen.coroutine
    def put(self, *args):
        if not self.put_tasks:
            self.raise404()
        response = yield self.task_handler.put_one(0, *args, **self.get_request_data())
        self.write(str(response.result))
        self.finish()

    @asynchronous
    @gen.coroutine
    def delete(self, *args):
        if not self.delete_tasks:
            self.raise404()
        response = yield self.task_handler.delete_one(0, *args, **self.get_request_data())
        self.write(str(response.result))
        self.finish()

    def raise403(self):
        raise tornado.web.HTTPError(403, 'Not enough permissions to perform this action')

    def raise404(self):
        raise tornado.web.HTTPError(404, 'Object not found')

    def raise405(self):
        raise tornado.web.HTTPError(405, 'Method Not Allowed')

    def get_request_uri(self):
        return self.request.uri

    def get_request_data(self):
        data = {}
        for arg in list(self.request.arguments.keys()):
            data[arg] = self.get_argument(arg)
            if data[arg] == '':  # Tornado 3.0+ compatibility
                data[arg] = None
        return data


class TCeleryAsyncHandler(tornado.web.RequestHandler, ptask_req_handler.TaskRequestHandler):
    @asynchronous
    @gen.coroutine
    def get(self, *args):
        if not self.get_tasks:
            self.raise404()
        self.task_handler.get_async(*args, **self.get_request_data())
        self.finish()

    @asynchronous
    @gen.coroutine
    def post(self, *args):
        if not self.post_tasks:
            self.raise404()
        self.task_handler.post_async(*args, **self.get_request_data())
        self.finish()

    @asynchronous
    @gen.coroutine
    def put(self, *args):
        if not self.put_tasks:
            self.raise404()
        self.task_handler.put_async(*args, **self.get_request_data())
        self.finish()

    @asynchronous
    @gen.coroutine
    def delete(self, *args):
        if not self.delete_tasks:
            self.raise404()
        self.task_handler.delete_async(*args, **self.get_request_data())
        self.finish()

    def raise403(self):
        raise tornado.web.HTTPError(403, 'Not enough permissions to perform this action')

    def raise404(self):
        raise tornado.web.HTTPError(404, 'Object not found')

    def raise405(self):
        raise tornado.web.HTTPError(405, 'Method Not Allowed')

    def get_request_uri(self):
        return self.request.uri

    def get_request_data(self):
        data = {}
        for arg in list(self.request.arguments.keys()):
            data[arg] = self.get_argument(arg)
            if data[arg] == '':  # Tornado 3.0+ compatibility
                data[arg] = None
        return data


def routes(route_list):
    return python_rest_handler.routes(route_list)

def tcelery_routes(uri_path, **kwargs):
    kwargs['base_handler'] = kwargs.get('base_handler', TCeleryReqHandler)
    #kwargs['module'] = kwargs.get('module', '.')

    # default only method get that mapped to uri_path
    tasks = kwargs['get_tasks'] = kwargs.get('get_tasks', [])
    kwargs['post_tasks'] = kwargs.get('post_tasks', [])
    kwargs['put_tasks'] = kwargs.get('put_tasks', [])
    kwargs['delete_tasks'] = kwargs.get('delete_tasks', [])

    return python_rest_handler.task_routes(uri_path, tasks, **kwargs)

def tcelery_async_routes(uri_path, **kwargs):
    kwargs['base_handler'] = kwargs.get('base_handler', TCeleryAsyncHandler)
    #kwargs['module'] = kwargs.get('module', '.')

    # default only method get that mapped to uri_path
    tasks = kwargs['get_tasks'] = kwargs.get('get_tasks', [])
    kwargs['post_tasks'] = kwargs.get('post_tasks', [])
    kwargs['put_tasks'] = kwargs.get('put_tasks', [])
    kwargs['delete_tasks'] = kwargs.get('delete_tasks', [])

    return python_rest_handler.task_routes(uri_path, tasks, **kwargs)
