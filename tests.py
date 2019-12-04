import os
from os import listdir

templates = ['404.html', 'about.html', 'addnote.html', 'base.html', 'editnote.html', 'edituser.html', 'index.html',
            'login.html', 'notes.html', 'register.html', 'singlenote.html', 'user.html']
important_files_folders = ['__init__.py', 'errors.py', 'forms.py', 'models.py', 'routes.py']

def check_pages_exist():
    real_templates = os.listdir('./app/templates')
    for template in templates:
        assert(template in real_templates)

def check_files_exist():
    app_files = os.listdir('./app')
    for file in important_files_folders:
        assert(file in app_files)

def check_files_do_not_exist():
    all_files = os.listdir('./')
    assert(not '.env' in all_files)
    assert(not 'app.db' in all_files)

def check_information_hidden():
    with open ('.flaskenv', 'r') as myfile:
        env = myfile.readlines()
        assert(not 'SECRET_KEY' in env)
        assert(not 'MAIL_PASSWORD' in env)
    myfile.close()

check_pages_exist()
check_files_exist()
check_files_do_not_exist()
check_information_hidden()
