import os
import tempfile
from time import sleep
from threading import Thread
from wsgiref.simple_server import WSGIServer, WSGIRequestHandler
from behave import fixture, use_fixture
from splinter import Browser
from flask_sqlalchemy import SQLAlchemy
from app import create_app, db

def before_all(context):
    WSGIServer.allow_reuse_address = True
    context.app = create_app(True)
    context.app.config['SERVER_HOST'] = os.environ.get('SERVER_HOST') or 'localhost'
    context.app.config['SERVER_PORT'] = os.environ.get('SERVER_PORT') or 5000
    context.app.config['SERVER_NAME'] = context.app.config['SERVER_HOST'] + ':' + str(context.app.config['SERVER_PORT'])
    context.browser = Browser('chrome')
    context.server = WSGIServer((context.app.config['SERVER_HOST'], int(context.app.config['SERVER_PORT'])), WSGIRequestHandler)
    context.server.set_app(context.app)
    context.thread = Thread(target=context.server.serve_forever)
    context.thread.start()

def after_all(context):
    context.server.shutdown()
    context.thread.join()
    context.browser.quit()

def before_scenario(context, scenario):
    context.request = context.app.test_request_context()
    context.client = context.app.test_client()
    context.context = context.app.app_context()
    with context.context:
        db.create_all()
    sleep(1)

def after_scenario(context, scenario):
	sleep(1)
	with context.context:
		context.browser.cookies.delete()
		db.drop_all()
