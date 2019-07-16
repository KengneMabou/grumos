# coding: utf-8 
'''
Created on 26 juil. 2016

@author: kengne
'''

from flask import Blueprint, request
from flask.views import MethodView
#from flask_mongoengine.wtf import model_form

auth_url_register = Blueprint('auth_urls', __name__, template_folder='../../view/web_assets/templates/')


# request handler.
class LogInView(MethodView):
    
   

    def get(self):
        from src.view.python_views.system.system import GrumosDefaultDialogue
        return GrumosDefaultDialogue().login()
    
    def post(self):
        
        from src.view.python_views.system.system import AuthDialogue
        
        login = request.form['username']
        password =request.form['password']
        return  AuthDialogue().validerFacteurAuth(login, password)
    

class LogOutView(MethodView):

    def get(self):
        from src.view.python_views.system.system import GrumosDefaultDialogue
        return GrumosDefaultDialogue().logout()

class RootView(MethodView):

    def get(self):
        from src.view.python_views.system.system import GrumosDefaultDialogue
        return GrumosDefaultDialogue().root()
    
class GrumosConsoleView(MethodView):

    def get(self):
        from src.view.python_views.system.system import GrumosDefaultDialogue
        return GrumosDefaultDialogue().ouvrir()


        
# Register the urls
auth_url_register.add_url_rule('/login/', view_func=LogInView.as_view('login_handler'))
auth_url_register.add_url_rule('/logout/', view_func=LogOutView.as_view('logout_handler'))
auth_url_register.add_url_rule('/', view_func=RootView.as_view('root_handler'))
auth_url_register.add_url_rule('/console/', view_func=GrumosConsoleView.as_view('console_index_handler'))



