# coding: utf-8 
'''
Created on 25 juil. 2016

@author: kengne
'''

import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask_script import Manager, Server
from application import app
from src.technique.mongo_engine.mongo_engine_odm import db
from src.technique.general_services.general_service import InitAppComponent

manager = Manager(app)

# Turn on debugger by default and reloader
manager.add_command("runserver", Server(
    use_debugger = True,
    use_reloader = True,
    host = '0.0.0.0')
)

manager.add_command("init_app", InitAppComponent())

if __name__ == "__main__":
    manager.run()

