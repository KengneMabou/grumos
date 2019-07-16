# coding: utf-8 
'''
Created on 14 oct. 2016

@author: kengne
'''
from src.view.python_views.utils.dialogue import GenericDialogue
from flask import render_template, redirect, url_for

class EditIncidentDialogue(GenericDialogue):
    
    name = ""
    description = ""
    machines_impacted = ""
    incident_type = ""
    services_impacted = ""
    gravity = ""
    confirm = "" 
    incident_date = ""
    resolution_date = "" 
    state = ""
    
    
    def create_incident(self, name, description, machines_impacted, incident_type, services_impacted, gravity, confirm, incident_date, resolution_date, state):
        
        from src.logic.evenement.incident_logic import IncidentLogic
        from src.logic.monitoring.monitoring_component_logic import MonitoringComponentLogic
        from src.logic.monitoring.services_component_logic import ServicesComponentLogic
        
        ilog = IncidentLogic()
        
        list_incident_type = ['network', 'system', "software service", "docker container"]
        list_gravity = ['minor', 'warning', 'critical']
        list_state = ['open', 'resolved', 'non resolved']
        
        mcl = MonitoringComponentLogic()
        scl = ServicesComponentLogic()
        
        list_machines = mcl.list_machines()
        list_services = scl.list_services()
        
        
        error = ilog.create_incident(name, description, machines_impacted, incident_type, services_impacted, gravity, confirm, incident_date, resolution_date, state)
        
        if not error:
            return IncidentDialogue().ouvrir_par_redirection()
        else:
            context_data = {"destination_url": url_for('incident_urls.new_incident_handler'),
                            "name": name,
                            "description": description,
                            "machines_impacted" : machines_impacted,
                            "incident_type" : incident_type,
                            "services_impacted" : services_impacted,
                            "gravity" : gravity, 
                            "confirm" : confirm, 
                            "incident_date" : incident_date, 
                            "resolution_date" : resolution_date, 
                            "state" : state,
                            "list_incident_type" : list_incident_type,
                            "list_machines" : list_machines,
                            "list_services" : list_services,
                            "list_gravity" : list_gravity,
                            "list_state" : list_state,
                            "update_mode":False,
                            "error":error,
                        }
            return self.ouvrir(context_data) 
        
        
        
        
    def update_incident(self, id_incident, name, description, machines_impacted, incident_type, services_impacted, gravity, confirm, incident_date, resolution_date, state):
        
        from src.logic.evenement.incident_logic import IncidentLogic
        from src.logic.monitoring.monitoring_component_logic import MonitoringComponentLogic
        from src.logic.monitoring.services_component_logic import ServicesComponentLogic
        
        ilog = IncidentLogic()
        
        list_incident_type = ['network', 'system', "software service", "docker container"]
        list_gravity = ['minor', 'warning', 'critical']
        list_state = ['open', 'resolved', 'non resolved']
        mcl = MonitoringComponentLogic()
        scl = ServicesComponentLogic()
        
        list_machines = mcl.list_machines()
        list_services = scl.list_services()
        
        error = ilog.update_incident(id_incident, name, description, machines_impacted, incident_type, services_impacted, gravity, confirm, incident_date, resolution_date, state)
        if not error:
            return IncidentDialogue().ouvrir_par_redirection()
        else:
            context_data = {"destination_url": url_for('incident_urls.update_incident_handler', id_incident=id_incident),
                            "name": name,
                            "description": description,
                            "machines_impacted" : machines_impacted,
                            "incident_type" : incident_type,
                            "services_impacted" : services_impacted,
                            "gravity" : gravity, 
                            "confirm" : confirm, 
                            "incident_date" : incident_date, 
                            "resolution_date" : resolution_date, 
                            "state" : state,
                            "list_incident_type" : list_incident_type,
                            "list_machines" : list_machines,
                            "list_services" : list_services,
                            "list_gravity" : list_gravity,
                            "list_state" : list_state,
                            "update_mode":True,
                            "error":error,
                        }
            return self.ouvrir(context_data)
    
     
    def ouvrir(self, context_data=None):
        
        return render_template('grumos_templates/event/incident/form_incident.html', **context_data)
    
    def ouvrir_par_redirection(self, context_data=None):
        return redirect(url_for('incident_urls.new_incident_handler'))
    
    
class IncidentDialogue(GenericDialogue):
    
    list_incidents = None
    
    def delete_incident(self, id_incident):
        from src.logic.evenement.incident_logic import IncidentLogic
        IncidentLogic().delete_incident(id_incident)
        return self.ouvrir_par_redirection()
    
    def root_cause(self, id_incident, timedelta):
        from src.logic.evenement.incident_logic import IncidentLogic
        
        data = IncidentLogic().root_cause(id_incident, timedelta)
        context = {
            "root_causes": data,
            "root_cause_url": url_for('incident_urls.root_cause_handler', id_incident = id_incident),
        }
        
        return render_template('grumos_templates/event/incident/incident_root_cause.html', **context) 
            
    def update_incident(self, id_incident):
        
        from src.logic.evenement.incident_logic import IncidentLogic
        from src.logic.monitoring.monitoring_component_logic import MonitoringComponentLogic
        from src.logic.monitoring.services_component_logic import ServicesComponentLogic
        
        ilog = IncidentLogic()
        
        list_incident_type = ['network', 'system', "software service", "docker container"]
        list_gravity = ['minor', 'warning', 'critical']
        list_state = ['open', 'resolved', 'non resolved']
        mcl = MonitoringComponentLogic()
        scl = ServicesComponentLogic()
        
        list_machines = mcl.list_machines()
        list_services = scl.list_services()
        
        context_data = {}
        
        incident = ilog.get_incident(id_incident)
        
        if incident : 
            
            context_data = {"destination_url": url_for('incident_urls.update_incident_handler', id_incident=incident.id),
                            "name": incident.name,
                            "description": incident.description,
                            "machines_impacted" : incident.machines_impacted,
                            "incident_type" : incident.incident_type,
                            "services_impacted" : incident.services_impacted,
                            "gravity" : incident.gravity, 
                            "confirm" : incident.confirm, 
                            "incident_date" : incident.incident_date, 
                            "resolution_date" : incident.resolution_date, 
                            "state" : incident.state,
                            "list_incident_type" : list_incident_type,
                            "list_machines" : list_machines,
                            "list_services" : list_services,
                            "list_gravity" : list_gravity,
                            "list_state" : list_state,
                            "update_mode":True,
                            "error":{},
                        }
        
        
        return EditIncidentDialogue().ouvrir(context_data)
    
    def create_incident(self):
    
        from src.logic.monitoring.monitoring_component_logic import MonitoringComponentLogic
        from src.logic.monitoring.services_component_logic import ServicesComponentLogic
        
        list_incident_type = ['network', 'system', "software service", "docker container"]
        list_gravity = ['minor', 'warning', 'critical']
        list_state = ['open', 'resolved', 'non resolved']
        mcl = MonitoringComponentLogic()
        scl = ServicesComponentLogic()
        
        list_machines = mcl.list_machines()
        list_services = scl.list_services()
        
        
        context_data = {"destination_url": url_for('incident_urls.new_incident_handler'),
                        "name": "",
                        "description": "",
                        "machines_impacted" : "",
                        "incident_type" : "",
                        "services_impacted" : "",
                        "gravity" : "", 
                        "confirm" : "", 
                        "incident_date" : "", 
                        "resolution_date" : "", 
                        "state" :"",
                        "list_incident_type" : list_incident_type,
                        "list_machines" : list_machines,
                        "list_services" : list_services,
                        "list_gravity" : list_gravity,
                        "list_state" : list_state,
                        "update_mode":False,
                        "error":{},
                    }
        
        return EditIncidentDialogue().ouvrir(context_data)
    
      
    def ouvrir (self, number_items, incident_type, page):
        
        from src.logic.evenement.incident_logic import IncidentLogic
        
        number_items = int(number_items)
        page = int(page) 
        data = IncidentLogic().filter_incidents(number_items, incident_type, page)

        list_incident_type = {"all":"Tous","network":"network", "system":"system", "software service":"software service", "docker container":"docker container"}
        list_number_items = [element * 10 for element in range(5)]
        next_page = page + 1
        previous_page = page - 1
        next_page = str(next_page)
        previous_page = str(previous_page)
        if incident_type is None:
            incident_type = "all"
        context = {
            "incidents": data,
            "number_items":number_items,
            "incident_type":incident_type,
            "page":page,
            "next_page": next_page,
            "previous_page": previous_page,
            "list_incident_type":list_incident_type,
            "list_number_items":list_number_items,
            "filtering_url": url_for('incident_urls.list_incident_handler'),
            "new_incident_url": url_for('incident_urls.new_incident_handler'),
        }
        
        return render_template('grumos_templates/event/incident/list_incident.html', **context)        
            

    
    def ouvrir_par_redirection(self, context_data=None):
        return redirect(url_for('incident_urls.list_incident_handler', number_items = 30, incident_type = "all", page=1))
