__author__ = 'rizki'

import ujson as json
import logging

from celery import Celery

from backend import celeryconfig

celery = Celery()
celery.config_from_object(celeryconfig)

# without database
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
    {'is_superadmin': 0, 'name': 'user3', 'photo': 'null', 'created_at': 1405424137, 'is_active': 1, 'updated_at': 1405424137, 'password': 'test', 'id': 3},
    {'is_superadmin': 0, 'name': 'user4', 'photo': 'null', 'created_at': 1405424137, 'is_active': 1, 'updated_at': 1405424137, 'password': 'test', 'id': 4},
    {'is_superadmin': 0, 'name': 'user5', 'photo': 'null', 'created_at': 1405424137, 'is_active': 1, 'updated_at': 1405424137, 'password': 'test', 'id': 5},
    {'is_superadmin': 0, 'name': 'user6', 'photo': 'null', 'created_at': 1405424137, 'is_active': 1, 'updated_at': 1405424137, 'password': 'test', 'id': 6},
    {'is_superadmin': 0, 'name': 'user7', 'photo': 'null', 'created_at': 1405424137, 'is_active': 1, 'updated_at': 1405424137, 'password': 'test', 'id': 7},
    {'is_superadmin': 0, 'name': 'user8', 'photo': 'null', 'created_at': 1405424137, 'is_active': 1, 'updated_at': 1405424137, 'password': 'test', 'id': 8},
    {'is_superadmin': 0, 'name': 'user9', 'photo': 'null', 'created_at': 1405424137, 'is_active': 1, 'updated_at': 1405424137, 'password': 'test', 'id': 9},
    {'is_superadmin': 0, 'name': 'user10', 'photo': 'null', 'created_at': 1405424137, 'is_active': 1, 'updated_at': 1405424137, 'password': 'test', 'id': 10}
    ]
    '''
    if not retval:
        return {}
    return str(retval)

@celery.task
def show_edit_delete_users(*args, **kwargs):
    if args:
        logging.info('args: %s' % args)
    if kwargs:
        logging.info('kwargs: %s' % kwargs)
    retval = '''
    {'is_superadmin': 0, 'name': 'user1', 'photo': 'null', 'created_at': 1405424137, 'is_active': 1, 'updated_at': 1405424137, 'password': 'test', 'id': 1}
    '''
    return str(retval)


"""
from playhouse import postgres_ext

from backend import model
import config

model.psqldb.initialize(postgres_ext.PostgresqlExtDatabase(config.default.db_name, user=config.default.db_user, password=config.default.db_password, host=config.default.db_ipaddr))

# using database
@celery.task
def list_create_users(*args, **kwargs):
    if args:
        logging.info('args: %s' % args)
    if kwargs:
        logging.info('kwargs: %s' % kwargs)
    #logging.info('method: %s' % method)
    users = model.User.select().limit(10).execute()
    retval = []
    for user in users:
        retval.append(str(user))
    if not retval:
        return {}
    return str(retval)

@celery.task
def show_edit_delete_users(*args, **kwargs):
    if args:
        logging.info('args: %s' % args)
    if kwargs:
        logging.info('kwargs: %s' % kwargs)
    #logging.info('method: %s' % method)
    try:
        id = int(args[0])
        retval = model.User.get(model.User.id == id)
    except model.User.DoesNotExist as e:
        #print 'does not exists'
        #raise e
        logging.warning(e)
        return {}
    return str(retval)
"""

if __name__ == "__main__":
    celery.start()
