# coding: utf-8 
'''
Created on 12 sept. 2016

@author: kengne
'''

from flask import Blueprint, request
from flask.views import MethodView
from src.technique.security.security import requires_session_auth, requires_permission

event_url_register = Blueprint('metric_urls', __name__, template_folder='../../view/web_assets/templates/')


       
class DeleteEventView(MethodView):
    
    
    @requires_session_auth
    @requires_permission("IT_ADMIN") 
    def get(self, id_event):
        from src.view.python_views.evenement.event import EventDialogue
        return EventDialogue().delete_event(id_event)
    

class ListEventsView(MethodView):

    @requires_session_auth
    @requires_permission("IT_ADMIN")
    def get(self):
        from src.view.python_views.system.system import GrumosDefaultDialogue
        event_type = request.args.get('event_type')
        number_items = request.args.get('number_items')
        page = request.args.get('page')
        
        if event_type == "all":
            event_type = None
        return GrumosDefaultDialogue().events(number_items, event_type, page)
    

class FilterEventsView(MethodView):

    @requires_session_auth
    @requires_permission("IT_ADMIN")
    def post(self):
        
        from src.view.python_views.evenement.event import EventDialogue
        
        number_items = request.form['number_items']
        event_type = request.form['event_type']
        
        if event_type == "all":
            event_type = None
            
        return EventDialogue().filter_event(number_items, event_type)
    
    
        

event_url_register.add_url_rule('/console/events/metrics/', view_func=ListEventsView.as_view('list_metric_handler'))
event_url_register.add_url_rule('/console/events/metrics/delete/<id_event>/', view_func=DeleteEventView.as_view('delete_metric_handler'))
event_url_register.add_url_rule('/console/events/metrics/filter/', view_func=FilterEventsView.as_view('filter_metric_handler'))
