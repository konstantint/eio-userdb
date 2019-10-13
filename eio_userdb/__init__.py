# -*- coding: UTF-8 -*-
"""
EIO user registration webapp

Copyright 2014, EIO Team.
License: MIT
"""
__version__ = '0.1'
import os
import logging.config

def main():
    import argparse
    parser = argparse.ArgumentParser(description='EIO-userdb webserver management and debug tool')
    parser.add_argument('-r', '--run', action='store_true', help='launch Flask built-in webserver')
    parser.add_argument('-c', '--config', metavar='<file.py>', action='store', help='read settings from the given .py file (overrides EIO_SETTINGS environement variable)')
    parser.add_argument('--createdb', action='store_true', help='create the database tables')
    parser.add_argument('--sample-data', action='store_true', help='insert sample data')
    parser.add_argument('--log-config', metavar='<file.cfg>', action='store', help='read python logging configuration from the given .cfg file')
    parser.add_argument('--version', action='version', version=__version__)
    args = parser.parse_args()
    if args.log_config is not None:
        logging.config.fileConfig(args.log_config)
    else:
        logging.basicConfig(level=logging.DEBUG)

    if args.config is not None:
        os.environ['EIO_SETTINGS'] = args.config
    if args.createdb:
        from .model import init_db
        init_db()
    if args.sample_data:
        from .model import init_sample_data
        init_sample_data()
    if args.run:
        from .main import app
        app.run(host=app.config['DEBUG_SERVER_HOST'], port=app.config['DEBUG_SERVER_PORT'])
    
    
