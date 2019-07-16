'''
Created on 25 juil. 2016

@author: kengne
'''

from flask import Flask
from src.technique.application_init.initializers import register_blueprints

app = Flask(__name__, static_url_path='', template_folder='../view/web_assets/templates/')

app.secret_key = 'KMHF@250390GRUMOSBYMYRA'
app.config['SESSION_TYPE'] = 'mongodb'

register_blueprints(app)

if __name__ == '__main__':
    app.run()
