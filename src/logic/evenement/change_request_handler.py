# coding: utf-8 
'''
Created on 12 sept. 2016

@author: kengne
'''

from flask import Blueprint, request
from flask.views import MethodView
from src.technique.security.security import requires_session_auth, requires_permission

change_url_register = Blueprint('change_urls', __name__, template_folder='../../view/web_assets/templates/')


class NewChangeView(MethodView):
    
    @requires_session_auth
    @requires_permission("IT_ADMIN")
    def get(self):
        from src.view.python_views.evenement.change import ChangeDialogue
        return ChangeDialogue().create_change()
    
    @requires_session_auth
    @requires_permission("IT_ADMIN")
    def post(self):
        
        from src.view.python_views.evenement.change import EditChangeDialogue
        
        name = request.form['name']
        description = request.form['description']
        machines_impacted = request.form.getlist('machines_impacted')
        change_type = request.form['change_type']
        services_impacted = request.form.getlist('services_impacted')
        change_date = request.form['change_date']
         
        return EditChangeDialogue().create_change(name, description, machines_impacted, change_type, services_impacted, change_date)

    

class UpdateChangeView(MethodView):

    @requires_session_auth
    @requires_permission("IT_ADMIN") 
    def get(self, id_change):
        from src.view.python_views.evenement.change import ChangeDialogue
        return ChangeDialogue().update_change(id_change)
    
    @requires_session_auth
    @requires_permission("IT_ADMIN") 
    def post(self, id_change):
        from src.view.python_views.evenement.change import EditChangeDialogue

        name = request.form['name']
        description = request.form['description']
        machines_impacted = request.form.getlist('machines_impacted', list())
        change_type = request.form['change_type']
        services_impacted = request.form.getlist('services_impacted', list())
        change_date = request.form['change_date']
        
        return EditChangeDialogue().update_change(id_change, name, description, machines_impacted, change_type, services_impacted, change_date)
       
class DeleteChangeView(MethodView):
    
    
    @requires_session_auth
    @requires_permission("IT_ADMIN") 
    def get(self, id_change):
        from src.view.python_views.evenement.change import ChangeDialogue
        return ChangeDialogue().delete_change(id_change)
    

class ListChangeView(MethodView):

    @requires_session_auth
    @requires_permission("IT_ADMIN")
    def get(self):
        from src.view.python_views.system.system import GrumosDefaultDialogue
        change_type = request.args.get('change_type')
        number_items = request.args.get('number_items')
        page = request.args.get('page')
        
        if change_type == "all":
            change_type = None
        return GrumosDefaultDialogue().changes(number_items, change_type, page)
    
    def post(self):
        from src.view.python_views.system.system import GrumosDefaultDialogue

        number_items = request.form['number_items']
        change_type = request.form['change_type']
        
        if change_type == "all":
            change_type = None
        
        return GrumosDefaultDialogue().changes(number_items, change_type, 1)
    
        
# Register the urls
change_url_register.add_url_rule('/console/events/changes/create', view_func=NewChangeView.as_view('new_change_handler'))
change_url_register.add_url_rule('/console/events/changes/update/<id_change>/', view_func=UpdateChangeView.as_view('update_change_handler'))
change_url_register.add_url_rule('/console/events/changes/', view_func=ListChangeView.as_view('list_change_handler'))
change_url_register.add_url_rule('/console/events/changes/delete/<id_change>/', view_func=DeleteChangeView.as_view('delete_change_handler'))
