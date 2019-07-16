# coding: utf-8 
'''
Created on 30 juil. 2016

@author: kengne
'''

import sys, os , inspect

current_path = os.path.realpath(os.path.abspath(os.path.dirname(inspect.getfile( inspect.currentframe()))))
for i in range(1,5): # remonter les repertoires parents
    current_path = os.path.dirname(current_path)

application_dir_path = current_path
#application_dir_path = os.path.join(current_path, '') #path with the ending '/'    
sys.path.insert(0, application_dir_path)

import unittest
from  application import app
from mongoengine import connect
from src.business.system.utilisateur import User


class UserMgtLogicTestCase(unittest.TestCase):
    
    def setUp(self):
        #from src.technique.mongo_engine.mongo_engine_odm import db
        with app.app_context():
            connect('grumos', host='mongomock://localhost')
            #connect('grumos', username='',password='',host='172.16.0.119')
            #connect('grumos', username='',password='',host='192.168.43.155')
        app.config['TESTING'] = True
        #app.config['HOST'] = "localhost:5000"
        self.app = app.test_client()
        #os.system("manager.py runserver")
        
        user = User.objects(login='meladodo II').first()
        if user : user.delete()
        
        user = User.objects(login='meladodo').first()
        if user : user.delete()

    def tearDown(self): 
    
        from src.business.system.utilisateur import User
        
        user = User.objects(login='meladodo II').first()
        if user : user.delete()
        
        user = User.objects(login='meladodo').first()
        if user : user.delete()
    
    
        
    def test_add_user(self):
        #test de l'ajout d'un utilisateur bien renseigné
        rv = self.get_user_form('/console/system/users/new/')
        assert 'user_form_new' in rv.data
        rv = self.add_user('kenmegne', 'fopoussi', 'kp@company.com', 'meladodo', 'meladodo', 'meladodo', 'IT_ADMIN')
        assert 'kenmegne' in rv.data
        
    def test_update_user(self):
        
        #test de la modification d'un utilisateur
        
        self.add_user('Administrator', 'Roots', 'root@company.com', 'admin', 'admin', 'admin', 'IT_ADMIN')
        
        self.add_user('kenmegne', 'fopoussi', 'kp@company.com', 'meladodo', 'meladodo', 'meladodo', 'IT_ADMIN')
        user = User.objects(login='meladodo').first()
        
        rv = self.get_user_form('/console/system/users/update/'+str(user.id)+'/')
        assert 'user_form_update' in rv.data
        
        rv = self.update_user('kenmegne II', 'fopoussi II', 'kp@company.com II', 'meladodo II', 'meladodo II', 'meladodo II', 'IT_ADMIN', 'meladodo')
        assert 'kenmegne II' in rv.data
        
        rv = self.update_user('kenmegne II', 'fopoussi II', 'kp@company.com II', 'admin', 'meladodo II', 'meladodo II', 'IT_ADMIN', 'meladodo II')
        assert 'Ce Login existe déjà' in rv.data
        
        rv = self.update_user('kenmegne II', 'fopoussi II', 'kp@company.com II', 'meladodo II', '', '', 'IT_ADMIN', 'meladodo II')
        assert 'Le mot de passe ne peut être vide' in rv.data
        
        rv = self.update_user('kenmegne II', 'fopoussi II', 'kp@company.com II', 'meladodo II', 'mimbangs', 'testo', 'IT_ADMIN', 'meladodo II')
        assert 'Les mots de passe ne correspondent' in rv.data
        
        
    
    def test_delete_user(self):
        #test de la modification d'un utilisateur
        
        self.add_user('kenmegne', 'fopoussi', 'kp@company.com', 'meladodo', 'meladodo', 'meladodo', 'IT_ADMIN')
        user = User.objects(login='meladodo').first()
        
        # On liste d'abord les utilisateurs pour détecter la présence de l'utilisateur ajouté mieux modifier dans les test d'jout et de modification d'utilisateur
        rv = self.app.get('/console/system/users/', follow_redirects=True)
        assert 'meladodo' in rv.data
        
        # on supprime l'utilisateur et on confirme qu'il n'est plus dans la liste des utilisateurs
        rv = self.app.get('/console/system/users/delete/'+str(user.id)+'/', follow_redirects=True)
        assert 'meladodo' not in rv.data
        
          
    def update_user(self, _name, _surname, _email, _login, _password, _passwordBis, _profile, previous_login):
        from src.business.system.utilisateur import User
        
        user = User.objects(login=previous_login).first()
        return self.app.post('/console/system/users/update/'+str(user.id)+'/', data=dict(
            name = _name,
            surname = _surname,
            email = _email,
            login = _login,
            password = _password,
            passwordBis = _passwordBis,
            profile = _profile,
        ), follow_redirects=True)
        
    def add_user(self, _name, _surname, _email, _login, _password, _passwordBis, _profile):
        return self.app.post('/console/system/users/new/', data=dict(
            name = _name,
            surname = _surname,
            email = _email,
            login = _login,
            password = _password,
            passwordBis = _passwordBis,
            profile = _profile,
        ), follow_redirects=True)
    
    def get_user_form(self, url=None):
        return self.app.get(url, follow_redirects=False)

        

if __name__ == '__main__':
    unittest.main()