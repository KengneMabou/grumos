# coding: utf-8 
'''
Created on 4 sept. 2016

@author: kengne
'''

from flask import Blueprint, request
from flask.views import MethodView
from src.technique.security.security import requires_session_auth, requires_permission

hcomponent_url_register = Blueprint('hcomponent_urls', __name__, template_folder='../../view/web_assets/templates/')


# request handler.
class NewHardComponentView(MethodView):
    
    @requires_session_auth
    @requires_permission("IT_ADMIN")
    def get(self):
        from src.view.python_views.monitoring.hard_component import HardComponentDialogue
        return HardComponentDialogue().create_component()
    
    @requires_session_auth
    @requires_permission("IT_ADMIN")
    def post(self):
        
        from src.view.python_views.monitoring.hard_component import EditHardComponentDialogue
        
        name = request.form['name']
        address = request.form['address']
        
        return EditHardComponentDialogue().create_component(name, address)

    

class UpdateHardComponentView(MethodView):

    @requires_session_auth
    @requires_permission("IT_ADMIN") 
    def get(self, id_component):
        from src.view.python_views.monitoring.hard_component import HardComponentDialogue
        return HardComponentDialogue().update_component(id_component)
    
    @requires_session_auth
    @requires_permission("IT_ADMIN") 
    def post(self, id_component):
        from src.view.python_views.monitoring.hard_component import EditHardComponentDialogue

        name = request.form['name']
        address = request.form['address']
        
        return EditHardComponentDialogue().update_component(id_component, name, address)

        
class DeleteHardComponentView(MethodView):
    
    
    @requires_session_auth
    @requires_permission("IT_ADMIN") 
    def get(self, id_component):
        from src.view.python_views.monitoring.hard_component import HardComponentDialogue
        return HardComponentDialogue().delete_component(id_component)
    
class DiscoverHardComponentView(MethodView):

    @requires_session_auth
    @requires_permission("IT_ADMIN")
    def get(self):
        from src.view.python_views.monitoring.hard_component import HardComponentDialogue
        return HardComponentDialogue().discover_components()
    
    @requires_session_auth
    @requires_permission("IT_ADMIN") 
    def post(self):
        from src.view.python_views.monitoring.hard_component import DiscoveredComponentDialogue

        ip_range = request.form['ip_range']
        
        
        return DiscoveredComponentDialogue().advanced_discover_component(ip_range)
    

class AddDiscoveredHComponentView(MethodView):

    @requires_session_auth
    @requires_permission("IT_ADMIN")
    def get(self, ref_component):
        from src.view.python_views.monitoring.hard_component import DiscoveredComponentDialogue
        return DiscoveredComponentDialogue().add_discover_component(ref_component)
    

class ListHardComponentView(MethodView):

    @requires_session_auth
    @requires_permission("IT_ADMIN")
    def get(self):
        from src.view.python_views.system.system import GrumosDefaultDialogue
        return GrumosDefaultDialogue().h_components()
    
class TrashHardComponentView(MethodView):

    @requires_session_auth
    @requires_permission("IT_ADMIN")
    def get(self, id_component):
        from src.view.python_views.monitoring.hard_component import HardComponentDialogue
        return HardComponentDialogue().trash_component(id_component)

class ViewTrashHComponentView(MethodView):

    @requires_session_auth
    @requires_permission("IT_ADMIN")
    def get(self):
        from src.view.python_views.monitoring.hard_component import HardComponentDialogue
        return HardComponentDialogue().view_trashed_components()

class RestoreHardComponentView(MethodView):

    @requires_session_auth
    @requires_permission("IT_ADMIN")
    def get(self, id_component):
        from src.view.python_views.monitoring.hard_component import TrashedComponentsDialogue
        return TrashedComponentsDialogue().restore_component(id_component)
    
    
    
        
# Register the urls
hcomponent_url_register.add_url_rule('/console/monitoring/hcomponents/', view_func=ListHardComponentView.as_view('list_hcomponent_handler'))
hcomponent_url_register.add_url_rule('/console/monitoring/hcomponents/delete/<id_component>/', view_func=DeleteHardComponentView.as_view('delete_hcomponent_handler'))
hcomponent_url_register.add_url_rule('/console/monitoring/hcomponents/new/', view_func=NewHardComponentView.as_view('new_hcomponent_handler'))
hcomponent_url_register.add_url_rule('/console/monitoring/hcomponents/update/<id_component>/', view_func=UpdateHardComponentView.as_view('update_hcomponent_handler'))
hcomponent_url_register.add_url_rule('/console/monitoring/hcomponents/discover/', view_func=DiscoverHardComponentView.as_view('discover_hcomponent_handler'))
hcomponent_url_register.add_url_rule('/console/monitoring/hcomponents/discover/add/<ref_component>/', view_func=AddDiscoveredHComponentView.as_view('add_discovered_hcomponent_handler'))
hcomponent_url_register.add_url_rule('/console/monitoring/hcomponents/trash/<id_component>/', view_func=TrashHardComponentView.as_view('trash_hcomponent_handler'))
hcomponent_url_register.add_url_rule('/console/monitoring/hcomponents/trash/', view_func=ViewTrashHComponentView.as_view('view_trashed_hcomponent_handler'))
hcomponent_url_register.add_url_rule('/console/monitoring/hcomponents/restore/<id_component>/', view_func=RestoreHardComponentView.as_view('restore_hcomponent_handler'))
