# coding: utf-8 
'''
Created on 26 juil. 2016

@author: kengne
'''

from flask import session
from src.technique.application_init.settings_vars import session_attrs, default_user
from src.business.system.utilisateur import User
import datetime
from mongoengine import Q


class AuthAppLogic:
    
    user = None
    
    def check_auth(self, username, secret_pass):
        """
        Cette methode permet de controler si la combinaison login / mot de passe fournit par l'utilisateur sont valides.
        """
        import hashlib
        #User.objects(login = default_user.get('login')).delete()
        total_user = User.objects.count()
        if total_user < 1:
            d_user = User(name=default_user.get('name'),surname=default_user.get('surname'), email=default_user.get('email'), login=default_user.get('login'), password=default_user.get('password'), profile=default_user.get('profile'))
            d_user.save()
             
        self.user = User.objects(Q(login=username) & Q(password=hashlib.sha1(secret_pass).hexdigest())).first()
        if self.user:
            return True
        return False 
    
    def valider(self, username, secret_pass):
        """
        Cette méthode permet de initialiser la connexion d'un nouvel utilisateur .
        """
        if self.check_auth(username, secret_pass):
            
            session[session_attrs.get('logged_in_attr')] = True
            session[session_attrs.get('user_id_attr')] = str(self.user.id)
            session[session_attrs.get('username_attr')] = username
            session[session_attrs.get('name_attr')] = self.user.name
            session[session_attrs.get('profile_attr')] = self.user.profile
            session[session_attrs.get('logintime_attr')] = datetime.datetime.now()
                
            return True
        
        return False
    
    def logout(self):
        
        """
        Cette méthode permet de vider la session de l'utilisateur à sa déconnexion.
        """
        session.pop(session_attrs.get('user_id_attr'), None)
        session.pop(session_attrs.get('logged_in_attr'), None)
        session.pop(session_attrs.get('username_attr'), None)
        session.pop(session_attrs.get('profile_attr'), None)
        session.pop(session_attrs.get('name_attr'), None)
        session.pop(session_attrs.get('logintime_attr'), None)
        session.pop("network_scan_results", None)
        

    def root(self):
        """
        Cette méthode gère l'accès à l'url racine (/) de Grumos .
        """
        from src.view.python_views.system.system import AuthDialogue, GrumosDefaultDialogue
        if session.get(session_attrs.get('logged_in_attr')):
            return GrumosDefaultDialogue().ouvrir_par_redirection()
        else:
            return AuthDialogue().ouvrir_par_redirection()