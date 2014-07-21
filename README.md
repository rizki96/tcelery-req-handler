===================
tcelery-req-handler
===================

Simple routing handler for tornado-celery implementation. All tornado request will be processed in celery task asynchronously,
with "fire and forget" style or "the handler waiting for result" style. This module depend on [tornado-celery module]
(https://github.com/mher/tornado-celery) and the code structure was taken from [python-rest-handler]
(https://github.com/paulocheque/python-rest-handler) and [tornado-rest-handler](https://github.com/paulocheque/tornado-rest-handler)
projects with some adjustments.


Prerequisites :
--------------
* RabbitMQ server (celery with redis is not supported)


Install :
---------
* pip install -U git+https://github.com/rizki96/tcelery-req-handler.git


How To Use :
------------
1. import tcelery and use tcelery.setup_nonblocking_producer() for activating python-celery module
2. there are 2 routes function that being used to map url and celery tasks :
    * tcelery_routes(uri_path, get_tasks=[], post_tasks=[], put_tasks=[], delete_tasks=[], handler=None)

        routes that will trigger celery tasks, default behaviour is tornado handler will wait for executed task
        - uri_path : tornado uri
        - get_tasks : tasks list that will be triggered by http get method
        - post_tasks : tasks list that will be triggered by http post method
        - put_tasks : tasks list that will be triggered by http put method
        - delete_tasks : tasks list that will be triggered by http delete method
        - handler : tornado handler to customize request, response and tasks that being executed, if None default handler will
                    be used
    * tcelery_async_routes(uri_path, get_tasks=[], post_tasks=[], put_tasks=[], delete_tasks=[], handler=None)

        routes that will trigger celery tasks, default behaviour is tornado handler won't wait for executed task, it will
        do "fire and forget" the tasks process
        - uri_path : tornado uri
        - get_tasks : tasks list that will be triggered by http get method
        - post_tasks : tasks list that will be triggered by http post method
        - put_tasks : tasks list that will be triggered by http put method
        - delete_tasks : tasks list that will be triggered by http delete method
        - handler : tornado handler to customize request, response and tasks that being executed, if None default handler will
                    be used
3. uri_path, get_tasks, post_tasks, put_tasks, delete_tasks is accessible inside handler as class member
4. sample project is being provided inside example directory. From example dir, run these command:
    ```
    "python main.py"
    ```
    ,
    ```
    "celery worker -A backend.v1 -Q payment_default1 --concurrency 2 --loglevel=INFO"
    ```
    and access the url:
    ```
    "http://localhost:8888/v1/user"
    ```


Custom Handler :
----------------
The routing option can have a handler that customize the web resources being produced. For example the web resources can
be delivered as json output, by setting content-type to "application/json". Or checking any other conditions such as checking
tasks that being executed. Below is the "GET" method example and the celery task that will return json, split the parameter
into _body parameter and _query parameter.

    ```
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

    @celery.task
    def list_create_users(*args, **kwargs):
        if args:
            logging.info('args: %s' % args)
        if kwargs:
            logging.info('kwargs: %s' % kwargs)
        retval = '''
        [
        {'is_superadmin': 0, 'name': 'user1', 'photo': 'null', 'created_at': 1405424137, 'is_active': 1, 'updated_at': 1405424137, 'password': 'test', 'id': 1},
        {'is_superadmin': 0, 'name': 'user2', 'photo': 'null', 'created_at': 1405424137, 'is_active': 1, 'updated_at': 1405424137, 'password': 'test', 'id': 2},
        ]
        '''
        if not retval:
            return {}
        return str(retval)
    ```

Notice the line ```response = yield self.task_handler.get_one(0, *args, **kwargs)``` from above, the task_handler will execute
the index 0 of "self.get_tasks" (previously get_tasks was being set on the routing option). Here is the method to execute
one task, many tasks, and async tasks for get, post, put and delete method.

    ```
    def get_one(self, index, *args, **kwargs)  # execute one task from get method

    def post_one(self, index, *args, **kwargs)  # execute one task from post method

    def put_one(self, index, *args, **kwargs)  # execute one task from put method

    def delete_one(self, index, *args, **kwargs)  # execute one task from delete method

    def get_many(self, *args, **kwargs)  # execute many tasks from get method

    def post_many(self, index, *args, **kwargs)  # execute many tasks from post method

    def put_many(self, index, *args, **kwargs)  # execute many tasks from put method

    def delete_many(self, index, *args, **kwargs)  # execute many tasks from delete method

    def get_async(self, *args, **kwargs)  # execute async tasks from get method

    def post_async(self, index, *args, **kwargs)  # execute async tasks from post method

    def put_async(self, index, *args, **kwargs)  # execute async tasks from put method

    def delete_async(self, index, *args, **kwargs)  # execute async tasks from delete method
    ```

All of the methods above can be accessed from self.task_handler object if the class is assigned as handler in celery_routes
option


Benchmarks :
------------
1. Setup
    * linux ubuntu virtualbox vm (2 processor, 3 GB memory), 1 tornado process, 1 celery queue
2. Result
    * Without database call, waiting for result :
      ```
      ab -n 1000 -c 500 http://localhost:8888/v1/user
      ```

        ```
        Concurrency Level:      500
        Time taken for tests:   18.564 seconds
        Complete requests:      1000
        Failed requests:        0
        Write errors:           0
        Total transferred:      1775000 bytes
        HTML transferred:       1588000 bytes
        Requests per second:    53.87 [#/sec] (mean)
        Time per request:       9282.242 [ms] (mean)
        Time per request:       18.564 [ms] (mean, across all concurrent requests)
        Transfer rate:          93.37 [Kbytes/sec] received

        Connection Times (ms)
                      min  mean[+/-sd] median   max
        Connect:        0  427 824.4     19    3008
        Processing:  2103 7900 2125.6   8279   12826
        Waiting:     2103 7900 2125.6   8278   12826
        Total:       2146 8327 2543.6   8280   13850
        ```
    * Using database call (postgresql hstore ext, peewee orm, psycopg2), waiting for result :
      ```
      ab -n 1000 -c 500 http://localhost:8888/v1/user
      ```

        ```
        Concurrency Level:      500
        Time taken for tests:   18.203 seconds
        Complete requests:      1000
        Failed requests:        0
        Write errors:           0
        Total transferred:      1722000 bytes
        HTML transferred:       1535000 bytes
        Requests per second:    54.94 [#/sec] (mean)
        Time per request:       9101.527 [ms] (mean)
        Time per request:       18.203 [ms] (mean, across all concurrent requests)
        Transfer rate:          92.38 [Kbytes/sec] received

        Connection Times (ms)
                      min  mean[+/-sd] median   max
        Connect:        0  383 700.8     17    3007
        Processing:   838 7859 3417.1   7414   13357
        Waiting:      837 7859 3417.1   7414   13357
        Total:        873 8242 3898.8   7487   14613
        ```
    * Fire and forget :
      ```
      ab -n 1000 -c 500 http://localhost:8888/v1/async_user
      ```

        ```
        Concurrency Level:      500
        Time taken for tests:   2.875 seconds
        Complete requests:      1000
        Failed requests:        0
        Write errors:           0
        Total transferred:      192000 bytes
        HTML transferred:       0 bytes
        Requests per second:    347.82 [#/sec] (mean)
        Time per request:       1437.539 [ms] (mean)
        Time per request:       2.875 [ms] (mean, across all concurrent requests)
        Transfer rate:          65.22 [Kbytes/sec] received

        Connection Times (ms)
                      min  mean[+/-sd] median   max
        Connect:        0  217 404.3      0    1002
        Processing:     9  628 663.4    272    2259
        Waiting:        9  628 663.4    272    2259
        Total:         42  845 893.4    273    2840
        ```
