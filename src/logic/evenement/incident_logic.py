# coding: utf-8 
'''
Created on 12 sept. 2016

@author: kengne
'''

class IncidentLogic:
    
    
    incident = None
    
    
    
    def root_cause(self, id_incident, timedelta):
        from src.business.evenement.evenement import Incident
        from src.business.evenement.evenement import Problem
        from src.business.evenement.evenement import Change
        from mongoengine import Q
        import datetime
        data = {}
        
        try:
            timedelta = int(timedelta)
        except ValueError:
            timedelta = 3600
        
        today = datetime.datetime.now()
        DD = datetime.timedelta(seconds=timedelta)
        earlier = today - DD
        incident_cause = Incident.objects(Q(incident_date__lte = today) & Q(incident_date__gte = earlier))
        change_cause = Change.objects(Q(change_date__lte = today) & Q(change_date__gte = earlier))
        problem_cause = Problem.objects(Q(problem_date__lte = today) & Q(problem_date__gte = earlier))
        
        data["incident_cause"] = incident_cause
        data["change_cause"] = change_cause
        data["problem_cause"] =  problem_cause
        data["incident_name"] = Incident.objects(id=id_incident).first().name
        
        return data

    
    def filter_incidents(self, number_items = 0, incident_type = None, page = 1):
        
        from src.business.evenement.evenement import Incident
        
        incidents = {}
        
        number_items = int(number_items)
        page = int(page) 
        
        if incident_type is None:
            incidents = Incident.objects
        else:
            incidents = Incident.objects(incident_type=incident_type)
            
        if number_items > 0:
            maxi = page*number_items
            mini = page*number_items - number_items
            incidents = incidents[mini:maxi]
            
            
        return incidents

    def delete_incident(self, id_incident):
        from src.business.evenement.evenement import Incident
        
        error = None
        incident = Incident.objects(id=id_incident).first()
        
        if incident :
            incident.delete()
        
        return error
    

    def get_incident(self, id_incident):
        from src.business.evenement.evenement import Incident
        
        ch = Incident.objects(id=id_incident).first()
        
        return ch
          
    def list_incidents(self):
        from src.business.evenement.evenement import Incident
        
        incidents = Incident.objects.all()
        
        return incidents


    def update_incident(self, id_incident, name, description, machines_impacted, incident_type, services_impacted, gravity, confirm, incident_date, resolution_date, state):
        """
            Method for updating infos about a incident
        """
        from src.business.evenement.evenement import Incident
            
        error = self.validate_form_update(id_incident, name, description, machines_impacted, incident_type, services_impacted, gravity, confirm, incident_date, resolution_date, state)
        if resolution_date == "":
            resolution_date = None
        if not error:
            incident =  Incident.objects(id=id_incident).first()
            incident.name = name
            incident.description = description
            incident.machines_impacted =machines_impacted
            incident.incident_type = incident_type
            incident.services_impacted = services_impacted
            incident.gravity = gravity
            incident.confirm = confirm
            incident.incident_date = incident_date
            incident.resolution_date = resolution_date
            incident.state = state            
            incident.save()
            
        return error
    
    def create_incident(self,name, description, machines_impacted, incident_type, services_impacted, gravity, confirm, incident_date, resolution_date, state):
        """This method is for registring a new incident"""
        from src.business.evenement.evenement import Incident, IncidentContext
        from flask import session
        from src.technique.application_init.settings_vars import session_attrs
        error = None
        if resolution_date == "":
            resolution_date = None
        for machine_name in machines_impacted:
            error = self.validate_form_create(name, description, machine_name, incident_type, services_impacted, gravity, confirm, incident_date, resolution_date, state)
            if not error:
                inc = Incident(name = name, description = description, machines_impacted = machine_name, incident_type = incident_type, services_impacted = services_impacted, gravity = gravity, confirm = confirm, incident_date = incident_date, resolution_date = resolution_date, state = state, detected_by = "user", incident_recorder = session[session_attrs.get('username_attr')])
                i_context = IncidentContext(name=inc.name).save()
                list_last_events = self.getIncidentEvents(machine_name, incident_date)
                for i_ev in list_last_events:
                    IncidentContext.objects(id=i_context.id).update_one(push__events = i_ev)
    
                inc.context = i_context
                inc.save()
        return error
        
    def validate_form_create(self, name, description, machine_name, incident_type, services_impacted, gravity, confirm, incident_date, resolution_date, state):
        
        """
        method for validating input data during incident creation process
        """
        
        error = None
          
        if name == "":
            if not error: 
                error = {}
            error["name_empty_error"] = u"Le nom de l'incident est obligatoire"
               
            
        if incident_date == "": #TODO , we are also going to put a regex-based control to see if the date has the correct format
            if not error: 
                error = {}
            error["incident_date_empty _error"] = u"la date de l'incident est obligatoire"
            
            
            
        return error
    
    def validate_form_update(self, id_incident,name, description, machine_name, incident_type, services_impacted, gravity, confirm, incident_date, resolution_date, state):
        
        """
        method for validating input data during incident udpate process
        """
        
        error = None
        
            
        if name == "":
            if not error: 
                error = {}
            error["name_empty_error"] = u"Le nom de incident est obligatoire"
               
            
        if incident_date == "": #TODO , we are also going to put a regex-based control to see if the date has the correct format
            if not error: 
                error = {}
            error["incident_date_empty _error"] = u"la date de l'incident est obligatoire"
            
            
        return error
    
    def getIncidentEvents(self, machine_name, incident_date):
        from src.business.evenement.evenement import Event
        from mongoengine import Q
        from datetime import datetime
        import time
        
        ev_date = None
        unix_date = int(time.mktime(datetime.strptime(incident_date, '%d/%m/%Y').timetuple())) * 1000
        ev = Event.objects(Q(unix_epoch_timestamp__lte = str(unix_date)) & Q(host=machine_name)).first()
        
        if ev is None:
            current_date = datetime.now() 
            ev_date = int(time.mktime(current_date.timetuple())) * 1000
            ev_date = str(ev_date)
        else:
            ev_date = ev.unix_epoch_timestamp
        return Event.objects(Q(unix_epoch_timestamp = ev_date) & Q(host=machine_name))                 
                         
    def getUniqueMetricTimeStamp(self):
        from src.business.evenement.evenement import Event
        
        l_metric_inst = Event.objects.distinct("unix_epoch_timestamp")
        
        return l_metric_inst
        
    
