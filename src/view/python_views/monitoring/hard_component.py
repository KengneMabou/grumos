# coding: utf-8 
'''
Created on 3 sept. 2016

@author: kengne
'''

from src.view.python_views.utils.dialogue import GenericDialogue
from flask import render_template, redirect, url_for

class EditHardComponentDialogue(GenericDialogue):
    
    name = ""
    address = ""
    
    
    def create_component(self, name, address):
        
        from src.logic.monitoring.monitoring_component_logic import MonitoringComponentLogic
        
        error = MonitoringComponentLogic().create_hard_component(name, address)
        
        if not error:
            return HardComponentDialogue().ouvrir_par_redirection()
        else:
            context_data = {"destination_url": url_for('hcomponent_urls.new_hcomponent_handler'),
                            "name": name,
                            "address": address,
                            "update_mode":False,
                            "error":error,
                        }
            return self.ouvrir(context_data)
        
        
        
        
    def update_component(self, id_component, name, address):
        
        from src.logic.monitoring.monitoring_component_logic import MonitoringComponentLogic
        
        error = MonitoringComponentLogic().update_hard_component(id_component, name, address)
        if not error:
            return HardComponentDialogue().ouvrir_par_redirection()
        else:
            context_data = {"destination_url": url_for('hcomponent_urls.update_hcomponent_handler', id_component=id_component),
                            "name": name,
                            "address": address,
                            "update_mode":True,
                            "error":error,
                        }
            return self.ouvrir(context_data)
    
     
    def ouvrir(self, context_data=None):
        
        return render_template('grumos_templates/monitoring/component/form_hcomponent.html', **context_data)
    
    def ouvrir_par_redirection(self, context_data=None):
        return redirect(url_for('hcomponent_urls.new_hcomponent_handler'))
    
    
class HardComponentDialogue(GenericDialogue):
    
    list_consoles = None
    
    def delete_component(self, id_component):
        from src.logic.monitoring.monitoring_component_logic import MonitoringComponentLogic
        MonitoringComponentLogic().delete_hard_component(id_component)
        return self.ouvrir_par_redirection()
            
    def update_component(self, id_component):
        
        from src.logic.monitoring.monitoring_component_logic import MonitoringComponentLogic
        context_data = {}
        component = MonitoringComponentLogic().get_hard_component(id_component)
        
        if component :  
            
            context_data = {"destination_url": url_for('hcomponent_urls.update_hcomponent_handler', id_component=component.id),
                            "name": component.name,
                            "address": component.address,
                            "update_mode":True,
                            "error":{},
                        }
        
        
        return EditHardComponentDialogue().ouvrir(context_data)
    
    def create_component(self):
        
        context_data = {"destination_url": url_for('hcomponent_urls.new_hcomponent_handler'),
                        "name": "",
                        "address": "",
                        "update_mode":False,
                        "error":{},
                    }
        
        return EditHardComponentDialogue().ouvrir(context_data)
    
    def discover_components(self):
    
        return DiscoveredComponentDialogue().ouvrir()
    
    def trash_component(self, id_component):
    
        from src.logic.monitoring.monitoring_component_logic import MonitoringComponentLogic
        MonitoringComponentLogic().trash_hard_component(id_component)
        return self.ouvrir_par_redirection()
    
    def view_trashed_components(self):
    
        return TrashedComponentsDialogue().ouvrir()

    
    def ouvrir (self, context_data=None):
        from src.logic.monitoring.monitoring_component_logic import MonitoringComponentLogic
        
        data = MonitoringComponentLogic().get_non_trashed_hcomponents()
            
        context = {
            "components": data,
            "new_hcomponent_url": url_for('hcomponent_urls.new_hcomponent_handler'),
            "trashed_hcomponents_url": url_for('hcomponent_urls.view_trashed_hcomponent_handler'),
            "discover_hcomponent_url": url_for('hcomponent_urls.discover_hcomponent_handler'),
        }
        
        return render_template('grumos_templates/monitoring/component/list_hcomponent.html', **context)        
            

    
    def ouvrir_par_redirection(self, context_data=None):
        return redirect(url_for('hcomponent_urls.list_hcomponent_handler'))
    

class TrashedComponentsDialogue(GenericDialogue):
    
    
    def ouvrir (self, context_data=None):
        from src.logic.monitoring.monitoring_component_logic import MonitoringComponentLogic
        
        data = MonitoringComponentLogic().get_trashed_hcomponents()
        
       
        context = {
                "components": data,
            }
        
        return render_template('grumos_templates/monitoring/component/trashed_hcomponent.html', **context)
    
    def restore_component(self, id_component):
    
        from src.logic.monitoring.monitoring_component_logic import MonitoringComponentLogic
        MonitoringComponentLogic().restore_hard_component(id_component)
        return self.ouvrir_par_redirection()
        
    def ouvrir_par_redirection(self, context_data=None):
        return redirect(url_for('hcomponent_urls.view_trashed_hcomponent_handler'))
    
    
class DiscoveredComponentDialogue(GenericDialogue):
    
    list_component = None
    
    
    
    def add_discover_component(self, ref_component):
        from src.logic.monitoring.monitoring_component_logic import MonitoringComponentLogic
        MonitoringComponentLogic().add_discovered_hcomponents(ref_component)
        return self.ouvrir_par_redirection()
    
    def advanced_discover_component(self, ip_range):
        
        
        return self.ouvrir(ip_range)
    
    
    def ouvrir (self, ip_range = "", context_data=None):
        from src.logic.monitoring.monitoring_component_logic import MonitoringComponentLogic
        from flask import session
        data = None
        if ip_range=="":
            if "network_scan_results" in session:
                data = session["network_scan_results"]
            else:
                data = {}
        else:
            data = MonitoringComponentLogic().discover_hard_components(ip_range)
            session["network_scan_results"] = data
       
        context = {
                "destination_url": url_for('hcomponent_urls.discover_hcomponent_handler'),
                "components": data,
                "ip_range":ip_range,
                'error':{},
            }
        
        return render_template('grumos_templates/monitoring/component/discovered_hcomponent.html', **context)  
            
            
    def ouvrir_par_redirection(self, context_data=None):
        return redirect(url_for('hcomponent_urls.discover_hcomponent_handler'))

