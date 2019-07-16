'''
Created on 26 juil. 2016

@author: kengne
'''
from functools import wraps
from flask import request, Response, session
from src.logic.system.auth_logic import AuthAppLogic
from src.technique.application_init.settings_vars import session_attrs
from src.view.python_views.system.system import AuthDialogue, PermissionDialogue


def authenticate_basic():
    """Sends a 401 response that enables basic auth"""
    return Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})
    
    
def requires_basic_auth(f):
        
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if auth is None or not AuthAppLogic().check_auth(auth.username, auth.password):
            return authenticate_basic()
        return f(*args, **kwargs)
    return decorated
    

def requires_session_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
            
        if session.get(session_attrs.get('logged_in_attr')) is None:
            return AuthDialogue().ouvrir_par_redirection()
        return f(*args, **kwargs)
    return decorated
    
    
def requires_permission(permission_name, entity_name = None,  user_id = None): # decorator parameter
    from src.business.system.utilisateur import User   
        
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs): # function parameter
            user_present = session.get(session_attrs.get('user_id_attr'))
            if user_present is None:
                return PermissionDialogue().ouvrir()
            else:
                user = User.objects(id=session.get(session_attrs.get('user_id_attr'))).first()
                if not user.has_permission(permission_name, entity_name):
                    return PermissionDialogue().ouvrir()
                
            return f(*args, **kwargs)
        return decorated
        
    return decorator