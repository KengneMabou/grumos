# coding: utf-8 
'''
Created on 4 sept. 2016

@author: kengne
'''

from flask import Blueprint, request
from flask.views import MethodView
from src.technique.security.security import requires_session_auth, requires_permission

scomponent_url_register = Blueprint('scomponent_urls', __name__, template_folder='../../view/web_assets/templates/')


# request handler.
class NewServiceComponentView(MethodView):
    
    @requires_session_auth
    @requires_permission("IT_ADMIN")
    def get(self):
        from src.view.python_views.monitoring.service_component import ServiceComponentDialogue
        return ServiceComponentDialogue().create_component()
    
    @requires_session_auth
    @requires_permission("IT_ADMIN")
    def post(self):
        
        from src.view.python_views.monitoring.service_component import EditServiceComponentDialogue
        
        name = request.form['name']
        description = request.form['description']
        
        return EditServiceComponentDialogue().create_component(name, description)

    

class UpdateServiceComponentView(MethodView):

    @requires_session_auth
    @requires_permission("IT_ADMIN") 
    def get(self, id_component):
        from src.view.python_views.monitoring.service_component import ServiceComponentDialogue
        return ServiceComponentDialogue().update_component(id_component)
    
    @requires_session_auth
    @requires_permission("IT_ADMIN") 
    def post(self, id_component):
        from src.view.python_views.monitoring.service_component import EditServiceComponentDialogue

        name = request.form['name']
        description = request.form['description']
        
        return EditServiceComponentDialogue().update_component(id_component, name, description)

        
class DeleteServiceComponentView(MethodView):
    
    
    @requires_session_auth
    @requires_permission("IT_ADMIN") 
    def get(self, id_component):
        from src.view.python_views.monitoring.service_component import ServiceComponentDialogue
        return ServiceComponentDialogue().delete_component(id_component)
    

class ListServiceComponentView(MethodView):

    @requires_session_auth
    @requires_permission("IT_ADMIN")
    def get(self):
        from src.view.python_views.system.system import GrumosDefaultDialogue
        return GrumosDefaultDialogue().s_components()
    
        
# Register the urls
scomponent_url_register.add_url_rule('/console/monitoring/scomponents/', view_func=ListServiceComponentView.as_view('list_scomponent_handler'))
scomponent_url_register.add_url_rule('/console/monitoring/scomponents/delete/<id_component>/', view_func=DeleteServiceComponentView.as_view('delete_scomponent_handler'))
scomponent_url_register.add_url_rule('/console/monitoring/scomponents/new/', view_func=NewServiceComponentView.as_view('new_scomponent_handler'))
scomponent_url_register.add_url_rule('/console/monitoring/scomponents/update/<id_component>/', view_func=UpdateServiceComponentView.as_view('update_scomponent_handler'))
