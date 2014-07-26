__author__ = 'rizki'

import logging

from tornado import gen

class TaskExecutor(object):

    def execute_one(self, task, method, *args, **kwargs):
        serializer = kwargs.pop('serializer', 'json')
        #serializer = kwargs.pop('serializer', 'msgpack')
        #serializer = kwargs.pop('serializer', 'pickle')
        kwargs['method'] = method
        #logging.info('args: %s, kwargs: %s' % (args, kwargs))
        return gen.Task(task.apply_async, args=args, serializer=serializer, kwargs=kwargs)

    def execute_many(self, tasks, method, *args, **kwargs):
        serializer = kwargs.pop('serializer', 'json')
        #serializer = kwargs.pop('serializer', 'msgpack')
        #serializer = kwargs.pop('serializer', 'pickle')
        executed_tasks = []
        kwargs['method'] = method
        #logging.info('args: %s, kwargs: %s' % (args, kwargs))
        for task in tasks:
            executed_tasks.append(gen.Task(task.apply_async, args=args, serializer=serializer, kwargs=kwargs))
        return executed_tasks

    def execute_async(self, tasks, method, *args, **kwargs):
        serializer = kwargs.pop('serializer', 'json')
        #serializer = kwargs.pop('serializer', 'msgpack')
        #serializer = kwargs.pop('serializer', 'pickle')
        kwargs['method'] = method
        #logging.info('args: %s, kwargs: %s' % (args, kwargs))
        for task in tasks:
            task.apply_async(args=args, serializer=serializer, kwargs=kwargs)


class TaskHandler(TaskExecutor):

    def __init__(self, request_handler):
        self.handler = request_handler

    def get_one(self, index, *args, **kwargs):
        return self.execute_one(self.handler.get_tasks[index], "GET", *args, **kwargs)

    def post_one(self, index, *args, **kwargs):
        return self.execute_one(self.handler.post_tasks[index], "POST", *args, **kwargs)

    def put_one(self, index, *args, **kwargs):
        return self.execute_one(self.handler.put_tasks[index], "PUT", *args, **kwargs)

    def delete_one(self, index, *args, **kwargs):
        return self.execute_one(self.handler.delete_tasks[index], "DELETE", *args, **kwargs)

    def get_many(self, *args, **kwargs):
        return self.execute_many(self.handler.get_tasks, "GET", *args, **kwargs)

    def post_many(self, *args, **kwargs):
        return self.execute_many(self.handler.post_tasks, "POST", *args, **kwargs)

    def put_many(self, *args, **kwargs):
        return self.execute_many(self.handler.put_tasks, "PUT", *args, **kwargs)

    def delete_many(self, *args, **kwargs):
        return self.execute_many(self.handler.delete_tasks, "DELETE", *args, **kwargs)

    def get_async(self, *args, **kwargs):
        return self.execute_async(self.handler.get_tasks, "GET", *args, **kwargs)

    def post_async(self, *args, **kwargs):
        return self.execute_async(self.handler.post_tasks, "POST", *args, **kwargs)

    def put_async(self, *args, **kwargs):
        return self.execute_async(self.handler.put_tasks, "PUT", *args, **kwargs)

    def delete_async(self, *args, **kwargs):
        return self.execute_async(self.handler.delete_tasks, "DELETE", *args, **kwargs)

class TaskRequestHandler(object):
    '''
    It will also receive from a metaclass the "rest_handler" attribute that contains a RestHandler instance.
    It will also receive the following booleans: new_enabled, show_enabled, list_enabled, edit_enabled, delete_enabled
    '''
    uri_path = None
    get_tasks = []
    post_tasks = []
    put_tasks = []
    delete_tasks = []
    def raise403(self): pass
    def raise404(self): pass
    def raise405(self): pass
    def get_request_uri(self): pass
    def get_request_data(self): return {}
    def redirect(self, url, permanent=False, status=None, **kwargs): pass


class TaskRequestHandlerMetaclass(type):
    def __init__(cls, name, bases, attrs):
        return super(TaskRequestHandlerMetaclass, cls).__init__(name, bases, attrs)

    def __call__(cls, *args):
        result = super(TaskRequestHandlerMetaclass, cls).__call__(*args)
        msg = 'RestRequestHandler classes (%s) requires the attribute "%s"'
        if not result.uri_path:
            raise NotImplementedError(msg % (cls.__name__, 'uri_path'))
        result.task_handler = TaskHandler(result)
        return result

TaskRequestHandler = TaskRequestHandlerMetaclass(TaskRequestHandler.__name__, TaskRequestHandler.__bases__, dict(TaskRequestHandler.__dict__))


def routes(route_list):
    routes = []
    for route in route_list:
        if isinstance(route, list):
            routes.extend(route)
        else:
            routes.append(route)
    return routes

dynamic_classes_cache = {}

def get_unique_handler_class_name(base_handler):
    base_name = base_handler.__name__
    class_name = base_name
    index = dynamic_classes_cache.setdefault(class_name, 1)
    unique_class_name = class_name + str(index)
    index += 1
    dynamic_classes_cache[class_name] = index
    return unique_class_name

def task_handler(uri_path, tasks, base_handler, handler=None, **kwargs):
    only = set(kwargs.get('only', []))
    exclude = set(kwargs.get('exclude', []))
    if not only:
        only = set(('get', 'post', 'put', 'delete'))
    available_methods = only - exclude

    attrs = {}
    attrs.update(kwargs)
    attrs['uri_path'] = uri_path
    attrs['get_tasks'] = tasks

    unique_class_name = get_unique_handler_class_name(base_handler)

    if handler:
        rest_handler_cls = type(unique_class_name, (handler, base_handler), attrs)
    else:
        rest_handler_cls = type(unique_class_name, (base_handler,), attrs)
    return rest_handler_cls

def task_routes(uri_path, tasks, base_handler, handler=None, **kwargs):
    handler = task_handler(uri_path, tasks, base_handler, handler=handler, **kwargs)
    routes = []

    route = (r'%s' % uri_path, handler)
    routes.append(route)

    return routes