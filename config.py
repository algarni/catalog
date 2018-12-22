#!/usr/bin/env python3

import os
basedir = os.path.abspath(os.path.dirname(__file__))

POSTGRES = {
	'user':'catalog',
	'pw': 'Cat#2018',
	'db':'catalog',
	'host':'localhost',
	'port': '5432',
}


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'my-secret'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
       'sqlite:///' + os.path.join(basedir, 'app.db')
    # SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{user}:{pw}@{host}:{port}/{db}'.format(**POSTGRES)
    SQLALCHEMY_TRACK_MODIFICATIONS = True

