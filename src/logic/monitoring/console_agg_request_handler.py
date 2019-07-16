# coding: utf-8 
'''
Created on 2 août 2016

@author: kengne
'''
from flask import Blueprint, request
from flask.views import MethodView
from src.technique.security.security import requires_session_auth, requires_permission

console_url_register = Blueprint('console_agg_urls', __name__, template_folder='../../view/web_assets/templates/')


# request handler.
class NewConsoleView(MethodView):
    
    @requires_session_auth
    @requires_permission("IT_ADMIN")
    def get(self):
        from src.view.python_views.monitoring.console_agg import ConsoleAggDialogue
        return ConsoleAggDialogue().create_console()
    
    @requires_session_auth
    @requires_permission("IT_ADMIN")
    def post(self):
        
        from src.view.python_views.monitoring.console_agg import EditConsoleDialogue
        
        name = request.form['name']
        location = request.form['location']
        port = request.form['port']
        path = request.form['path']
        
        return EditConsoleDialogue().create_console(name, location, port, path)

    

class UpdateConsoleView(MethodView):

    @requires_session_auth
    @requires_permission("IT_ADMIN") 
    def get(self, id_console):
        from src.view.python_views.monitoring.console_agg import ConsoleAggDialogue
        return ConsoleAggDialogue().update_console(id_console)
    
    @requires_session_auth
    @requires_permission("IT_ADMIN") 
    def post(self, id_console):
        from src.view.python_views.monitoring.console_agg import EditConsoleDialogue

        name = request.form['name']
        location = request.form['location']
        port = request.form['port']
        path = request.form['path']
        
        return EditConsoleDialogue().update_console(id_console, name, location, port, path)

        
class DeleteConsoleView(MethodView):
    
    
    @requires_session_auth
    @requires_permission("IT_ADMIN") 
    def get(self, id_console):
        from src.view.python_views.monitoring.console_agg import ConsoleAggDialogue
        return ConsoleAggDialogue().delete_console(id_console)
    
class ViewConsolesView(MethodView):

    @requires_session_auth
    @requires_permission("IT_ADMIN")
    def get(self):
        from src.view.python_views.monitoring.console_agg import ConsoleAggDialogue
        return ConsoleAggDialogue().view_consoles()

class ListConsolesView(MethodView):

    @requires_session_auth
    @requires_permission("IT_ADMIN")
    def get(self):
        from src.view.python_views.system.system import GrumosDefaultDialogue
        return GrumosDefaultDialogue().console_agg()
    
    
        
# Register the urls
console_url_register.add_url_rule('/console/monitoring/consoles/', view_func=ListConsolesView.as_view('list_console_handler'))
console_url_register.add_url_rule('/console/monitoring/consoles/delete/<id_console>/', view_func=DeleteConsoleView.as_view('delete_console_handler'))
console_url_register.add_url_rule('/console/monitoring/consoles/new/', view_func=NewConsoleView.as_view('new_console_handler'))
console_url_register.add_url_rule('/console/monitoring/consoles/update/<id_console>/', view_func=UpdateConsoleView.as_view('update_console_handler'))
console_url_register.add_url_rule('/console/monitoring/consoles/view/', view_func=ViewConsolesView.as_view('view_console_handler'))




