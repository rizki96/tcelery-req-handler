__author__ = 'rizki'

import ujson as json
import logging

from celery import Celery
from playhouse import postgres_ext

from backend import celeryconfig, model

import config

celery = Celery()
celery.config_from_object(celeryconfig)

model.psqldb.initialize(postgres_ext.PostgresqlExtDatabase(config.default.db_name, user=config.default.db_user, password=config.default.db_password, host=config.default.db_ipaddr))

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


if __name__ == "__main__":
    celery.start()