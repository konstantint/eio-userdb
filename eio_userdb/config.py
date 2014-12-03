# -*- coding: UTF-8 -*-
"""
EIO user registration webapp :: Configuration

Copyright 2014, EIO Team.
License: MIT
"""
import os

class Config(object):
    # Development settings
    DEBUG = True
    SQLALCHEMY_ECHO = True
    MAIL_SUPPRESS_SEND = False
    
    # App settings
    SECRET_KEY = '\xf5\xfd\x94\x90\x9d\xd6;{\xb5l-}^(\xfc?\xbdW\xc6\t'
    SECRET_PASSWORD = 's3cr3t'
    CONTEST_ID = 1
    CONTEST_TITLE = u'Eesti Informaatika Olümpiaad'
    REGISTRATION_SERVER_URL = 'http://localhost:5000/'
    CONTEST_SERVER_URL = 'http://eio-contest.us.to/'
    CONTACT_URL = 'http://eio.ut.ee/'
    
    # Database connection
    SQLALCHEMY_DATABASE_URI = 'sqlite:///%s' % os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'db.sqlite')
    
    # Deployment option
    APPLICATION_ROOT = '/'  # Untested
    DEBUG_SERVER_HOST = '0.0.0.0'
    DEBUG_SERVER_PORT = 5000
    
    # Flask-mail config
    MAIL_SERVER = 'localhost'
    MAIL_PORT = 25 
    MAIL_USE_TLS = False
    MAIL_USE_SSL = False
    MAIL_USERNAME = None
    MAIL_PASSWORD = None
    MAIL_DEFAULT_SENDER = 'Eesti Informaatika Olympiaadide Server <kt@ut.ee>'
    MAIL_MAX_EMAILS = None
    MAIL_ASCII_ATTACHMENTS = False
    
    # Should not be changed
    # Enable string translation in forms    
    WTF_I18N_ENABLED = True
