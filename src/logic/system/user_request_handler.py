# coding: utf-8 
'''
Created on 2 août 2016

@author: kengne
'''
from flask import Blueprint, request
from flask.views import MethodView
from src.technique.security.security import requires_session_auth, requires_permission

user_url_register = Blueprint('user_urls', __name__, template_folder='../../view/web_assets/templates/')


# request handler.
class NewUserView(MethodView):
    
    @requires_session_auth
    @requires_permission("IT_ADMIN")
    def get(self):
        from src.view.python_views.system.system import UsersDialogue
        return UsersDialogue().create_user()
    
    @requires_session_auth
    @requires_permission("IT_ADMIN")
    def post(self):
        
        from src.view.python_views.system.system import EditUserDialogue
        
        name = request.form['name']
        surname = request.form['surname']
        email = request.form['email']
        login = request.form['login']
        password = request.form['password']
        passwordBis = request.form['passwordBis']
        profile = request.form['profile']
        
        return EditUserDialogue().create_user(name, surname, email, login, password, passwordBis, profile)

    

class UpdateUserView(MethodView):

    @requires_session_auth
    @requires_permission("IT_ADMIN") 
    def get(self, id_user):
        from src.view.python_views.system.system import UsersDialogue
        return UsersDialogue().update_user(id_user)
    
    @requires_session_auth
    @requires_permission("IT_ADMIN") 
    def post(self, id_user):
        from src.view.python_views.system.system import EditUserDialogue

        name = request.form['name']
        surname = request.form['surname']
        email = request.form['email']
        login = request.form['login']
        password = request.form['password']
        passwordBis = request.form['passwordBis']
        profile = request.form['profile']
        
        return EditUserDialogue().update_user(id_user, name, surname, email, login, password, passwordBis, profile)

class ProfileView(MethodView):

    @requires_session_auth
    def get(self, id_user):
        from src.view.python_views.system.system import GrumosDefaultDialogue
        return GrumosDefaultDialogue().profile(id_user)
    
    @requires_session_auth
    def post(self, id_user):
        from src.view.python_views.system.system import EditUserDialogue

        name = request.form['name']
        surname = request.form['surname']
        email = request.form['email']
        login = request.form['login']
        password = request.form['password']
        passwordBis = request.form['passwordBis']  
        return EditUserDialogue().update_user_profile(id_user, name, surname, email, login, password, passwordBis)
        
class DeleteUserView(MethodView):
    
    
    @requires_session_auth
    @requires_permission("IT_ADMIN") 
    def get(self, id_user):
        from src.view.python_views.system.system import UsersDialogue
        return UsersDialogue().delete_user(id_user)
    

class ListUsersView(MethodView):

    @requires_session_auth
    @requires_permission("IT_ADMIN")
    def get(self):
        from src.view.python_views.system.system import GrumosDefaultDialogue
        return GrumosDefaultDialogue().users()
    
    
        
# Register the urls
user_url_register.add_url_rule('/console/system/users/', view_func=ListUsersView.as_view('list_user_handler'))
user_url_register.add_url_rule('/console/system/users/delete/<id_user>/', view_func=DeleteUserView.as_view('delete_user_handler'))
user_url_register.add_url_rule('/console/system/users/new/', view_func=NewUserView.as_view('new_user_handler'))
user_url_register.add_url_rule('/console/system/users/update/<id_user>/', view_func=UpdateUserView.as_view('update_user_handler'))
user_url_register.add_url_rule('/profile/<id_user>/', view_func=ProfileView.as_view('profile_handler'))



