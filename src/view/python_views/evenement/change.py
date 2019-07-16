# coding: utf-8 
'''
Created on 14 oct. 2016

@author: kengne
'''
from src.view.python_views.utils.dialogue import GenericDialogue
from flask import render_template, redirect, url_for

class EditChangeDialogue(GenericDialogue):
    
    name = ""
    description = ""
    machines_impacted = ""
    change_type = ""
    services_impacted = ""
    change_date = ""
    
    def create_change(self, name, description, machines_impacted, change_type, services_impacted, change_date):
        
        from src.logic.evenement.change_logic import ChangeLogic
        from src.logic.monitoring.monitoring_component_logic import MonitoringComponentLogic
        from src.logic.monitoring.services_component_logic import ServicesComponentLogic
        
        chl = ChangeLogic()
        mcl = MonitoringComponentLogic()
        scl = ServicesComponentLogic()
        
        list_change_type = ['configuration change', 'service deployment']
        list_machines = mcl.list_machines()
        list_services = scl.list_services()
        
        error = chl.create_change(name, description, machines_impacted, change_type, services_impacted, change_date)
        
        if not error:
            return ChangeDialogue().ouvrir_par_redirection()
        else:
            context_data = {"destination_url": url_for('change_urls.new_change_handler'),
                            "name": name,
                            "description": description,
                            "machines_impacted" : machines_impacted,
                            "change_type" : change_type,
                            "services_impacted" : services_impacted,
                            "change_date" : change_date,
                            "list_change_type" : list_change_type,
                            "list_machines" : list_machines,
                            "list_services" : list_services,
                            "update_mode":False,
                            "error":error,
                        }
            return self.ouvrir(context_data) 
        
        
        
        
    def update_change(self, id_change, name, description, machines_impacted, change_type, services_impacted, change_date):
        
        from src.logic.evenement.change_logic import ChangeLogic
        from src.logic.monitoring.monitoring_component_logic import MonitoringComponentLogic
        from src.logic.monitoring.services_component_logic import ServicesComponentLogic
        
        chl = ChangeLogic()
        mcl = MonitoringComponentLogic()
        scl = ServicesComponentLogic()
        
        list_change_type = ['configuration change', 'service deployment']
        list_machines = mcl.list_machines()
        list_services = scl.list_services()
        
        error = chl.update_change(id_change, name, description, machines_impacted, change_type, services_impacted, change_date)
        if not error:
            return ChangeDialogue().ouvrir_par_redirection()
        else:
            context_data = {"destination_url": url_for('change_urls.update_change_handler', id_change=id_change),
                            "name": name,
                            "description": description,
                            "machines_impacted" : machines_impacted,
                            "change_type" : change_type,
                            "services_impacted" : services_impacted,
                            "change_date" : change_date,
                            "list_change_type" : list_change_type,
                            "list_machines" : list_machines,
                            "list_services" : list_services,
                            "update_mode":True,
                            "error":error,
                        }
            return self.ouvrir(context_data)
    
     
    def ouvrir(self, context_data=None):
        
        return render_template('grumos_templates/event/change/form_change.html', **context_data)
    
    def ouvrir_par_redirection(self, context_data=None):
        return redirect(url_for('change_urls.new_change_handler'))
    
    
class ChangeDialogue(GenericDialogue):
    
    list_changes = None
    
    def delete_change(self, id_change):
        from src.logic.evenement.change_logic import ChangeLogic
        ChangeLogic().delete_change(id_change)
        return self.ouvrir_par_redirection()
            
    def update_change(self, id_change):
        
        from src.logic.evenement.change_logic import ChangeLogic
        from src.logic.monitoring.monitoring_component_logic import MonitoringComponentLogic
        from src.logic.monitoring.services_component_logic import ServicesComponentLogic
        
        context_data = {}
        chl = ChangeLogic()
        change = chl.get_change(id_change)
        mcl = MonitoringComponentLogic()
        scl = ServicesComponentLogic()
        
        list_change_type = ['configuration change', 'service deployment']
        list_machines = mcl.list_machines()
        list_services = scl.list_services()
        if change : 
            
            context_data = {"destination_url": url_for('change_urls.update_change_handler', id_change=change.id),
                            "name": change.name,
                            "description": change.description,
                            "machines_impacted" : change.machines_impacted,
                            "change_type" : change.change_type,
                            "services_impacted" : change.services_impacted,
                            "change_date" : change.change_date,
                            "list_change_type" : list_change_type,
                            "list_machines" : list_machines,
                            "list_services" : list_services,
                            "update_mode":True,
                            "error":{},
                        }
        
        
        return EditChangeDialogue().ouvrir(context_data)
    
    def create_change(self):
        from src.logic.monitoring.monitoring_component_logic import MonitoringComponentLogic
        from src.logic.monitoring.services_component_logic import ServicesComponentLogic
        
        mcl = MonitoringComponentLogic()
        scl = ServicesComponentLogic()
        
        list_change_type = ['configuration change', 'service deployment']
        list_machines = mcl.list_machines()
        list_services = scl.list_services()
        
        context_data = {"destination_url": url_for('change_urls.new_change_handler'),
                        "name": "",
                        "description": "",
                        "machines_impacted" : "",
                        "change_type" : "",
                        "services_impacted" : "",
                        "change_date" : "",
                        "list_change_type" : list_change_type,
                        "list_machines" : list_machines,
                        "list_services" : list_services,
                        "update_mode":False,
                        "error":{},
                    }
        
        return EditChangeDialogue().ouvrir(context_data)
    
      
    def ouvrir (self, number_items, change_type, page):
        
        from src.logic.evenement.change_logic import ChangeLogic
        
        number_items = int(number_items)
        page = int(page) 
        data = ChangeLogic().filter_changes(number_items, change_type, page)
        #data = EventLogic().naive_list_events()
        list_change_type = {"all":"Tous","configuration change":"configuration change", "service deployment":"service deployment"}
        list_number_items = [element * 10 for element in range(5)]
        next_page = page + 1
        previous_page = page - 1
        next_page = str(next_page)
        previous_page = str(previous_page)
        if change_type is None:
            change_type = "all"
        context = {
            "changes": data,
            "number_items":number_items,
            "change_type":change_type,
            "page":page,
            "next_page": next_page,
            "previous_page": previous_page,
            "list_change_type":list_change_type,
            "list_number_items":list_number_items,
            "filtering_url": url_for('change_urls.list_change_handler'),
            "new_change_url": url_for('change_urls.new_change_handler'),
        }
        
        return render_template('grumos_templates/event/change/list_change.html', **context)        
            

    
    def ouvrir_par_redirection(self, context_data=None):
        return redirect(url_for('change_urls.list_change_handler', number_items = 30, change_type = "all", page=1))
