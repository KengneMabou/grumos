# coding: utf-8 
'''
Created on 30 juil. 2016

@author: kengne
'''

import sys, os, inspect

current_path = os.path.realpath(os.path.abspath(os.path.dirname(inspect.getfile( inspect.currentframe()))))
for i in range(1,5): # remonter les repertoires parents
    current_path = os.path.dirname(current_path)
application_dir_path = current_path
#application_dir_path = os.path.join(current_path, '') #path with the ending '/'    
sys.path.insert(0, application_dir_path)

import unittest
from  application import app
from mongoengine import connect


class AuthLogicTestCase(unittest.TestCase):
    
    def setUp(self):
        #from src.technique.mongo_engine.mongo_engine_odm import db
        with app.app_context():
            connect('grumos', host='mongomock://localhost')
            #connect('grumos', username='',password='',host='192.168.43.155')
        app.config['TESTING'] = True
        #app.config['HOST'] = "localhost:5000"
        self.app = app.test_client()
        #os.system("manager.py runserver")

    def tearDown(self):
    
        pass
    
        
    def test_login_logout(self):
        #test de la connexion à grumos avec les bon identifiant: ce test devrait passer
        rv = self.login('admin', 'admin')
        assert 'console_grumos' in rv.data
        
        #test de la déconnexion à grumos avec de mauvais identifiant: ce test devrait passer
        rv = self.login('admin', 'adminkmhf')
        assert 'auth_error' in rv.data
        
        #test de la déconnexion à grumos
        rv = self.logout()
        self.assertTrue('login_form' in rv.data)
          
    
    def login(self, username, password):
        return self.app.post('/login/', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.app.get('/logout/', follow_redirects=True)
        

if __name__ == '__main__':
    unittest.main()