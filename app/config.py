# config.py

import os

class BaseConfig(object):
    SECRET_KEY = os.environ['SECRET_KEY']
    DEBUG = os.environ['DEBUG']
    DB_NAME = os.environ['DB_NAME']
    DB_USER = os.environ['DB_USER']
    DB_PASS = os.environ['DB_PASS']
    DB_SERVICE = os.environ['DB_SERVICE']
    DB_PORT = os.environ['DB_PORT']

    RDFSERVER_BASE_URI = os.environ['RDFSERVER_BASE_URI']
    RDFSERVER_PORT = os.environ['RDFSERVER_PORT']

    SPARQL_LIMIT = os.environ['SPARQL_LIMIT']

