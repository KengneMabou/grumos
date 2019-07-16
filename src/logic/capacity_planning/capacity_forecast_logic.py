# coding: utf-8 
'''
Created on 17 sept. 2016

@author: kengne
'''
from mongoengine import Q
class CapacityForcastLogic:
    
    def getListMetricInstances(self):
        """
        This method is to get the list of distinct metric instance in perf data / event collection
        """
        from src.business.evenement.evenement import Event
        
        l_metric_inst = Event.objects.distinct("metric_instance")
        
        return l_metric_inst
    
    def getListPluginInstances(self):
        """
        This method is to get the list of individual plugin instance in perf data / event collection
        """
        from src.business.evenement.evenement import Event
        
        l_plug_inst = Event.objects.distinct("plugin_instance")
        
        return l_plug_inst
    
    def getListMachineInstances(self):
        """
        This method is to get the list of distinct plugin instance in perf data / event collection
        """
        from src.business.evenement.evenement import Event
        
        l_machine_inst = Event.objects.distinct("host")
        
        return l_machine_inst
    
    def getListTypeInstances(self):
        """
        This method is to get the list of distinct type instance in perf data / event collection
        """
        from src.business.evenement.evenement import Event
        
        l_type_inst = Event.objects.distinct("type_instance")
        
        return l_type_inst
    
    def getListPlugin(self):
        """
        This method is to get the list of distinct plugin in perf data / event collection
        """
        from src.business.evenement.evenement import Event
        
        l_plugin = Event.objects.distinct("plugin")
        
        return l_plugin
    
    
    def getPluginInstanceByMetricInstance(self):
        """
        This method is to get the list of individual type instance in perf data / event collection
        """
        from src.business.evenement.evenement import Event
        
        result = Event.objects.aggregate({
            "$group":{"_id":"$metric_instance","plugin_instance":{"$addToSet":"$plugin_instance"}}                                           
        })
        
        return list(result)
        
    def getMetricInstanceByPlugin(self):
        """
        This method is to get the list of individual type instance in perf data / event collection
        """
        from src.business.evenement.evenement import Event
        
        result = Event.objects.aggregate({
            "$group":{"_id":"$plugin","metric_instance":{"$addToSet":"$metric_instance"}}                                           
        })
        
        return list(result)
    
    def getTypeInstanceByMetricInstance(self):
        """
        This method is to get the list of individual type instance in perf data / event collection
        """
        from src.business.evenement.evenement import Event
        
        result = Event.objects.aggregate({
            "$group":{"_id":"$metric_instance","type_instance":{"$addToSet":"$type_instance"}}                                           
        })
        
        return list(result)
    
    
    
    def is_pluginInstance_matched_metricInstance(self, metric_instance, plugin_instance):
        """
        This method is to verify if a metric instance match a plugin instnce
        """
        from src.business.evenement.evenement import Event
        
        res = Event.objects(Q(metric_instance=metric_instance) & Q(plugin_instance=plugin_instance)).first()
        
        if res:
            return True
        
        return False
    
    def is_typeInstance_matched_metricInstance(self, metric_instance, type_instance):
        """
        This method is to verify if a metric instance match a type instnce
        """
        from src.business.evenement.evenement import Event
        
        res = Event.objects(Q(metric_instance=metric_instance) & Q(type_instance=type_instance)).first()
        
        if res:
            return True
        
        return False
    
    
    
    def capacityForcaster(self, data_collect_interval, pattern_period, number_past_season_observed, t_forecast, equipement_observed, metric_instance_observed, plugin_instance_observed, type_instance_observed, past_time_to_plot):
        
        from src.logic.capacity_planning.forecasting import GrumosForecastiong
        
        no_error = True
        alpha = 0.716 
        beta = 0.029
        gamma = 0.993 
        error= {}
        data = None
        forecasted_data = None
        previous_data = None
        slen = 24*3600 # season lenght: Default to 1 day
        n_preds = 100 # number of next point to forcast
        result = {"data":None, "error":None}
        serie_bundle = self.getSerie(equipement_observed, metric_instance_observed, plugin_instance_observed, type_instance_observed)
        serie =  serie_bundle["raw_values"]
        events =  serie_bundle["raw_events"]
        try:
            data_collect_interval = int(data_collect_interval)
        except ValueError:
            
            no_error = False
            if not error: 
                error = {}
            error['data_collect_interval'] = u"L'intervalle de collecte de données doit être un entier"
        
        try:
            pattern_period = int(pattern_period)
        except ValueError:
            
            no_error = False
            if not error: 
                error = {}
            error['pattern_period'] = u"La durée d'une saison de données doit être un entier"
            
        try:
            number_past_season_observed = int(number_past_season_observed)
        except ValueError:
            
            no_error = False
            if not error: 
                error = {}
            error['number_past_season_observed'] = u"Le nombre de saison de données à observer doit être un entier"
        
        
        try:
            t_forecast = int(t_forecast)
        except ValueError:
            
            no_error = False
            if not error: 
                error = {}
            error['t_forecast'] = u"La periode de temps à prédire doit être un entier"
            
        if not self.is_typeInstance_matched_metricInstance(metric_instance_observed, type_instance_observed):
            no_error = False
            if not error: 
                error = {}
            error['metric_instance_type_instance_no_matched'] = u"L'indicateur de suivi choisi ne correspond pas à la métrique choisi"
            
        if not self.is_pluginInstance_matched_metricInstance(metric_instance_observed, plugin_instance_observed):
            no_error = False
            if not error: 
                error = {}
            error['metric_instance_plugin_instance_no_matched'] = u"Le composant choisi ne correspond pas à la métrique choisi"


        if not self.is_pattern_period_good(data_collect_interval, pattern_period):
            no_error = False
            if not error: 
                error = {}
            error['season_length_aberration'] = u"Impossible de calculer le saisonnalité des données: La durée d'une saison doit être 3 fois la durée de l'intervalle de collecte de données"
        else:
            slen = self.compute_season_length(data_collect_interval, pattern_period)
            
        
        n_point_observed = self.number_data_point_observed(slen, number_past_season_observed)
        working_serie = serie[:n_point_observed+1]
        working_event = events[:n_point_observed+1]
        working_serie.reverse()
        last_observe_event = working_event.first() # last observe events when 'events' var is MongoEngine QuerySet
        working_event.order_by("+unix_epoch_timestamp")
        if not self.has_at_least_2_season_lenght(working_serie, slen):
            no_error = False
            if not error: 
                error = {}
            error['insufficient_data_points'] = u"Il n'y pas suffisamment de données pour satisfaire aux critères de prévision suggérer, veuillez en suggerer d'autres"
        
        if no_error:
            n_preds = self.number_data_point_forecasted(t_forecast, data_collect_interval)
            
            data = GrumosForecastiong().additiveHoltWinters(working_serie, slen, alpha, beta, gamma, n_preds)
            forecasted_data = self.formatFutureDataForPlotting(int(last_observe_event.unix_epoch_timestamp), data[n_point_observed:])
            previous_data = self.formatPastDataForPlotting(working_event, past_time_to_plot, data_collect_interval)
        
        result["error"] = error
        result["observed_and_forecasted_data"] = data
        result["forecasted_data"] = forecasted_data
        result["previous_data"] = previous_data
        #result["previous_data"] = self.formatPastDataForPlotting(working_event, 7*24*3600, 10)
        return result
            
         
    def has_at_least_2_season_lenght(self, serie,slen):
        
        if len(serie) >= (2*slen):
            return True
        return False
    
    def is_pattern_period_good(self, data_collect_interval, pattern_period):
        
        if pattern_period >= 3*data_collect_interval:
            return True
        
        return False
    
    def compute_season_length(self, data_collect_interval, pattern_period):
        return int(pattern_period / data_collect_interval)
    
    def getSerie(self,equipement_observed, metric_instance_observed, plugin_instance_observed, type_instance_observed):
        from src.business.evenement.evenement import Event
        ret = {"raw_values":None,"raw_events":None}
        serie = list()
        ev_l = list()
        res = Event.objects(Q(host=equipement_observed) & Q(plugin_instance=plugin_instance_observed) & Q(type_instance=type_instance_observed) & Q(metric_instance=metric_instance_observed))
        for item in res:
            serie.append(item.value)
            ev_l.append(item)
        
        ret["raw_values"] = serie   
        ret["raw_events"] = res
        ret["events_list"] = ev_l
        
        return ret
        
    
    def formatFutureDataForPlotting(self, begin_date, values):
        
        import datetime
        """
        We suppose here that "values" argument is ordered from the past to recent event and "begin_date' is in millisecond
        
        """
        row = None
        res = list()
        begin_date = int(begin_date/1000)
        for val in values:
            begin_date = begin_date + 10
            ev_date = datetime.datetime.fromtimestamp(begin_date).strftime('%Y-%m-%d %H:%M:%S')
            row = {"date":ev_date, "raw_value":val}
            res.append(row)
        
        return res
    
    def formatPastDataForPlotting(self, events, n_seconds_past = None, data_collect_interval = None):
        import datetime
        """
        We suppose here that "events" argument is ordered from the past to recent event
        """
        try:
            n_seconds_past = int (n_seconds_past)
        except ValueError:
            n_seconds_past =300 
        n_past_point = None
        row = None
        res = list()
        working_ev = None
        if n_seconds_past is not None and data_collect_interval is not None and self.previous_period_good(n_seconds_past, data_collect_interval):
            n_past_point = int(n_seconds_past/data_collect_interval)
        if n_past_point is None:
            working_ev = events
        else:
            begin = len(events)-n_past_point
            if begin < 0:
                begin = 0  
            working_ev = events[begin:len(events)]
            
        for evt in working_ev:
            
            ev_date = datetime.datetime.fromtimestamp(int(int(evt.unix_epoch_timestamp)/1000)).strftime('%Y-%m-%d %H:%M:%S')
            row = {"date":ev_date, "raw_value":evt.value}
            res.append(row)
       
    
        return res
    
    
    def number_data_point_forecasted(self, t_forecast, data_collect_interval):
        if self.forecast_period_good(t_forecast, data_collect_interval):
            return int(t_forecast/data_collect_interval)
        else:
            return 1
    
    def number_data_point_observed(self, slen, number_past_season_observed):
        
        return slen * number_past_season_observed
    
    def forecast_period_good(self, t_forecast, data_collect_interval):
        
        if t_forecast >= data_collect_interval:
            return True
        return False
        
    def previous_period_good(self, n_seconds_past, data_collect_interval):
        
        if n_seconds_past >= data_collect_interval:
            return True
        return False
        
        
        
    
    