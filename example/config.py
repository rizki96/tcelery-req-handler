__author__ = 'rizki'

# -*- coding: utf-8 -*-
"""
List of configuration variables and enumerations used throughout the app.
"""

import os


_d = {
    "cookie_secret": "d3t1kfr4m3w0rk",
    "debug": False,
    "server_ipaddr": "0.0.0.0",
    "server_port": 8888,
    "db_name": "payment",
    "db_ipaddr": "localhost",
    "db_port": "5432",
    "db_user": "postgres",
    "db_password": "",
    "lite_db": "db/default.db",
    "use_cache": False,
    "redis_ipaddr": 'localhost',
    "redis_port": 8889,
    "redis_expire": 60,
    "base_path":os.path.join(os.path.dirname(__file__), "static"),
    "log_search": False,
    #"static_base_url": "http://localhost/static",
    #"static_path": os.path.join(os.path.dirname(__file__), "static"),
    #"geoip_dat": os.path.join(os.path.dirname(__file__), "GeoIP.dat"),
}


class AppConfig:
    """
    Class holding all configurations necessary for the app to run.

    The values are accessible as attributes of an instance of this class.
    When you access an attribute, its value is at first looked up in the
    enviroment variables (key is uppercased). If it is not found there,
    the class checks a config dictionary passed to it at init. If the value
    is not even there, it returns None.
    """

    def __init__(self, config_dict):
        self.values = config_dict

    def __getattr__(self, name):
        """
        Get the value from the ENV, if it's not present, get
        it from the dictionary. Returns None if not found.
        """
        return os.environ.get(name.upper(), self.values.get(name.lower()))

default = AppConfig(_d)
