import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'is_this_even_needed'
