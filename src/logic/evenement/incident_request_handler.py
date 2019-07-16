# coding: utf-8 
'''
Created on 12 sept. 2016

@author: kengne
'''

from flask import Blueprint, request
from flask.views import MethodView
from src.technique.security.security import requires_session_auth, requires_permission

incident_url_register = Blueprint('incident_urls', __name__, template_folder='../../view/web_assets/templates/')


class NewIncidentView(MethodView):
    
    @requires_session_auth
    @requires_permission("IT_ADMIN")
    def get(self):
        from src.view.python_views.evenement.incident import IncidentDialogue
        return IncidentDialogue().create_incident()
    
    @requires_session_auth
    @requires_permission("IT_ADMIN")
    def post(self):
        
        from src.view.python_views.evenement.incident import EditIncidentDialogue
        
        name = request.form['name']
        description = request.form['description']
        machines_impacted = request.form.getlist('machines_impacted')
        incident_type = request.form['incident_type']
        services_impacted = request.form.getlist('services_impacted')
        gravity = request.form['gravity']
        confirm = request.form['confirm']
        incident_date = request.form['incident_date']
        resolution_date = request.form['resolution_date']
        state = request.form['state']
        
        if confirm == "on":
            confirm = True
        else:
            confirm = False
         
        return EditIncidentDialogue().create_incident(name, description, machines_impacted, incident_type, services_impacted, gravity, confirm, incident_date, resolution_date, state)

    

class UpdateIncidentView(MethodView):

    @requires_session_auth
    @requires_permission("IT_ADMIN") 
    def get(self, id_incident):
        from src.view.python_views.evenement.incident import IncidentDialogue
        return IncidentDialogue().update_incident(id_incident)
    
    @requires_session_auth
    @requires_permission("IT_ADMIN") 
    def post(self, id_incident):
        from src.view.python_views.evenement.incident import EditIncidentDialogue

        name = request.form['name']
        description = request.form['description']
        machines_impacted = request.form['machines_impacted']
        incident_type = request.form['incident_type']
        services_impacted = request.form.getlist('services_impacted')
        gravity = request.form['gravity']
        confirm = request.form['confirm']
        incident_date = request.form['incident_date']
        resolution_date = request.form['resolution_date']
        state = request.form['state']
        
        if confirm == "on":
            confirm = True
        else:
            confirm = False
        
        return EditIncidentDialogue().update_incident(id_incident, name, description, machines_impacted, incident_type, services_impacted, gravity, confirm, incident_date, resolution_date, state)
       
class DeleteIncidentView(MethodView):
    
    
    @requires_session_auth
    @requires_permission("IT_ADMIN") 
    def get(self, id_incident):
        from src.view.python_views.evenement.incident import IncidentDialogue
        return IncidentDialogue().delete_incident(id_incident)
    

class ListIncidentView(MethodView):

    @requires_session_auth
    @requires_permission("IT_ADMIN")
    def get(self):
        from src.view.python_views.system.system import GrumosDefaultDialogue
        incident_type = request.args.get('incident_type')
        number_items = request.args.get('number_items')
        page = request.args.get('page')
        
        if incident_type == "all":
            incident_type = None
        return GrumosDefaultDialogue().incidents(number_items, incident_type, page)
    
    def post(self):
        from src.view.python_views.system.system import GrumosDefaultDialogue

        number_items = request.form['number_items']
        incident_type = request.form['incident_type']
        
        if incident_type == "all":
            incident_type = None
        
        return GrumosDefaultDialogue().incidents(number_items, incident_type, 1)

class RootCauseIncidentView(MethodView):
    
    
    @requires_session_auth
    @requires_permission("IT_ADMIN") 
    def get(self, id_incident):
        from src.view.python_views.evenement.incident import IncidentDialogue
        return IncidentDialogue().root_cause(id_incident, 3600)
    
    def post(self, id_incident):
        from src.view.python_views.evenement.incident import IncidentDialogue

        timedelta = request.form['timedelta']
        
        return IncidentDialogue().root_cause(id_incident, timedelta)
    
        
# Register the urls
incident_url_register.add_url_rule('/console/events/incidents/create', view_func=NewIncidentView.as_view('new_incident_handler'))
incident_url_register.add_url_rule('/console/events/incidents/update/<id_incident>/', view_func=UpdateIncidentView.as_view('update_incident_handler'))
incident_url_register.add_url_rule('/console/events/incidents/', view_func=ListIncidentView.as_view('list_incident_handler'))
incident_url_register.add_url_rule('/console/events/incidents/delete/<id_incident>/', view_func=DeleteIncidentView.as_view('delete_incident_handler'))
incident_url_register.add_url_rule('/console/events/incidents/root_cause/<id_incident>/', view_func=RootCauseIncidentView.as_view('root_cause_handler'))
