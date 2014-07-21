__author__ = 'rizki'

import datetime
#import json
import ujson as json
import logging
import calendar

from peewee import Proxy, Model
from playhouse import postgres_ext
#from playhouse.signals import Model as SignaledModel, pre_save, post_save

psqldb = Proxy()

class PgAppModel(Model):
    class Meta:
        database = psqldb

    created_at = postgres_ext.DateTimeField(default=datetime.datetime.now)
    updated_at = postgres_ext.DateTimeField()

    def save(self, *args, **kwargs):
        self.updated_at = datetime.datetime.now()
        return super(AppModel, self).save(*args, **kwargs)

    def __str__(self):
        r = {}
        for k in self._data.keys():
            try:
                if type(getattr(self, k)) == bool:
                    r[k] = 1 if getattr(self,k) == True else 0
                elif type(getattr(self, k)) == int:
                    r[k] = int(getattr(self, k))
                elif type(getattr(self, k)) == long:
                    r[k] = long(getattr(self, k))
                elif type(getattr(self, k)) == datetime.datetime:
                    r[k] = calendar.timegm(getattr(self, k).timetuple())
                elif getattr(self, k) == None:
                    r[k] = NULL
                else:
                    r[k] = str(getattr(self, k))
            except:
                r[k] = json.dumps(getattr(self, k))
        return str(r)

class User(PgAppModel):
    name = postgres_ext.CharField(unique=True, null=False)
    password = postgres_ext.CharField()
    photo = postgres_ext.BlobField(null=True)
    is_superadmin = postgres_ext.BooleanField(default=False)
    is_active = postgres_ext.BooleanField(default=False)


from playhouse import apsw_ext

class AWPTimeField(apsw_ext.TimeField):
    def __init__(self, *args, **kwargs):
        super(AWPTimeField, self).__init__(*args, **kwargs)

class AWPDateField(apsw_ext.DateField):
    def __init__(self, *args, **kwargs):
        super(AWPDateField, self).__init__(*args, **kwargs)

class AWPDateTimeField(apsw_ext.DateTimeField):
    def __init__(self, *args, **kwargs):
        super(AWPDateTimeField, self).__init__(*args, **kwargs)

sqlitedb = Proxy()

class SqliteAppModel(apsw_ext.Model):
    class Meta:
        database = sqlitedb

    created_at = AWPDateTimeField(default=datetime.datetime.now)
    updated_at = AWPDateTimeField()

    def save(self, *args, **kwargs):
        self.updated_at = datetime.datetime.now()
        return super(SqliteAppModel, self).save(*args, **kwargs)

    def __str__(self):
        r = {}
        for k in self._data.keys():
            try:
                if type(getattr(self, k)) == bool:
                    r[k] = 1 if getattr(self,k) == True else 0
                elif type(getattr(self, k)) == int:
                    r[k] = int(getattr(self, k))
                elif type(getattr(self, k)) == long:
                    r[k] = long(getattr(self, k))
                elif type(getattr(self, k)) == datetime.datetime:
                    r[k] = calendar.timegm(getattr(self, k).timetuple())
                elif getattr(self, k) == None:
                    r[k] = NULL
                else:
                    r[k] = str(getattr(self, k))
            except:
                r[k] = json.dumps(getattr(self, k))
        return str(r)

class SqUser(SqliteAppModel):
    name = apsw_ext.CharField(unique=True, null=False)
    password = apsw_ext.CharField()
    photo = apsw_ext.BlobField(null=True)
    is_superadmin = apsw_ext.BooleanField(default=False)
    is_active = apsw_ext.BooleanField(default=False)

