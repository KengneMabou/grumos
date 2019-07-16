# coding: utf-8 
'''
Created on 12 sept. 2016

@author: kengne
'''

from flask import Blueprint, request
from flask.views import MethodView
from src.technique.security.security import requires_session_auth, requires_permission

incident_forecast_url_register = Blueprint('incident_forecast_urls', __name__, template_folder='../../view/web_assets/templates/')

         
class FilterForecastsView(MethodView):
    
    
    @requires_session_auth
    @requires_permission("IT_ADMIN")
    def get(self):
        from src.view.python_views.system.system import GrumosDefaultDialogue
        return GrumosDefaultDialogue().incidents_forecast()

    @requires_session_auth
    @requires_permission("IT_ADMIN")
    def post(self):
        from src.view.python_views.evenement.incident_forecast import IncidentForecastDialogue
        
        data_collect_interval = request.form['data_collect_interval']
        pattern_period = request.form['pattern_period']
        
        number_past_season_observed = request.form['number_past_season_observed']
        t_forecast = request.form['t_forecast']
        
        equipement_observed = request.form['equipement_observed']
        metric_instance_observed = request.form['metric_instance_observed']
        
        plugin_instance_observed = request.form['plugin_instance_observed']
        type_instance_observed = request.form['type_instance_observed']
        past_time_to_plot = request.form['past_time_to_plot']
        
        return IncidentForecastDialogue().filter_incident_forecast(data_collect_interval, pattern_period, number_past_season_observed, t_forecast, equipement_observed, metric_instance_observed, plugin_instance_observed, type_instance_observed, past_time_to_plot)
        
    
    
        
# Register the urls

incident_forecast_url_register.add_url_rule('/console/events/incidents/forecast/', view_func=FilterForecastsView.as_view('incident_forecast_handler'))
#forecast_url_register.add_url_rule('/console/capacity_planning/capacity_forecast/', view_func=ListForecastsView.as_view('list_forecast_handler'))
