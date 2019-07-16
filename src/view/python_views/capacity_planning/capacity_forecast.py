# coding: utf-8 
'''
Created on 21 sept. 2016

@author: kengne
'''
from src.view.python_views.utils.dialogue import GenericDialogue
from flask import render_template, redirect, url_for

class CapacityForecastDialogue(GenericDialogue):
    
    data_collection_speed = None
    pattern_period = None
    number_past_seasons = None
    prevision_interval = None #  we will add 15 seconds to this value and will remove the point forcasted corresponding to the value time period added
    prevision_equipement = None
    metric_instance_forecasted = None # Eg: "disk_octets"
    plugin_instance_forecasted = None # Eg: "sda"
    type_instance_forecasted = None # Eg: "read"
    plugin_forecasted = None #Eg: "disk"
    
    
    def filter_capacity_forecast (self, data_collect_interval, pattern_period, number_past_season_observed, t_forecast, equipement_observed, metric_instance_observed, plugin_instance_observed, type_instance_observed, past_time_to_plot):
    
        return self.ouvrir(data_collect_interval, pattern_period, number_past_season_observed, t_forecast, equipement_observed, metric_instance_observed, plugin_instance_observed, type_instance_observed, past_time_to_plot)
            
    
    
    def ouvrir (self, data_collect_interval = None, pattern_period = None, number_past_season_observed = None, t_forecast = None, equipement_observed = None, metric_instance_observed = None, plugin_instance_observed = None, type_instance_observed= None, past_time_to_plot = None):
        from src.logic.capacity_planning.capacity_forecast_logic import CapacityForcastLogic 
        
        c_logic = CapacityForcastLogic()
        
        list_metric_instance = c_logic.getListMetricInstances()
        list_plugin_instance = c_logic.getListPluginInstances()
        list_type_instance = c_logic.getListTypeInstances()
        list_plugin = c_logic.getListPlugin()
        list_equipements = c_logic.getListMachineInstances()
        metric_instance_by_plugin = c_logic.getMetricInstanceByPlugin()
        plugin_instance_by_metric_instance = c_logic.getPluginInstanceByMetricInstance()
        type_instance_by_metric_instance = c_logic.getTypeInstanceByMetricInstance()
        
        if equipement_observed is None:
            try:
                equipement_observed = list_equipements[0]
            except:
                equipement_observed = ""
        
        if type_instance_observed is None:
            try:
                type_instance_observed = list_type_instance[0]
            except:
                type_instance_observed = ""
                
        if plugin_instance_observed is None:
            try:
                plugin_instance_observed = list_plugin_instance[0]
            except:
                plugin_instance_observed = ""
        
        if metric_instance_observed is None:    
            try:
                metric_instance_observed = list_metric_instance[0]
            except:
                metric_instance_observed = ""
        
        
        if data_collect_interval is None:
            data_collect_interval = 15 # 10 secondes
        if pattern_period is None:
            pattern_period = 120 # 120 seconde
        if number_past_season_observed is None:
            number_past_season_observed = 5
        if t_forecast is None:
            t_forecast = 600 # periode of time in future to forecast 
        if past_time_to_plot is None:
            past_time_to_plot = 600 # periode of time in past to plot
        res = CapacityForcastLogic().capacityForcaster(data_collect_interval, pattern_period, number_past_season_observed, t_forecast, equipement_observed, metric_instance_observed, plugin_instance_observed, type_instance_observed, past_time_to_plot)
        
        
        
        context = {
            "forecasted_data": res['forecasted_data'],
            "previous_data": res['previous_data'],
            "list_plugin_instance": list_plugin_instance,
            "list_metric_instance":list_metric_instance,
            "list_equipements":list_equipements,
            "list_type_instance": list_type_instance,
            "list_plugin":list_plugin,
            "equipement_observed":equipement_observed,
            "type_instance_observed":type_instance_observed,
            "plugin_instance_observed":plugin_instance_observed,
            "metric_instance_observed":metric_instance_observed,
            "data_collect_interval":data_collect_interval,
            "pattern_period":pattern_period,
            "number_past_season_observed":number_past_season_observed,
            "t_forecast":t_forecast,
            "past_time_to_plot":past_time_to_plot,
            "metric_instance_by_plugin":metric_instance_by_plugin,
            "plugin_instance_by_metric_instance":plugin_instance_by_metric_instance,
            "type_instance_by_metric_instance":type_instance_by_metric_instance,
            "filtering_url": url_for('forecast_urls.filter_forecast_handler'),
            "error":res['error']
        }
        
        return render_template('grumos_templates/capacity_planning/capacity_forecast/list_capacity_forecast.html', **context)        
            

    
    def ouvrir_par_redirection(self, context_data=None):
        return redirect(url_for('forecast_urls.filter_forecast_handler'))