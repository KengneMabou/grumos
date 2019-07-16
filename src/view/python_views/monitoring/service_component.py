# coding: utf-8 
'''
Created on 3 sept. 2016

@author: kengne
'''

from src.view.python_views.utils.dialogue import GenericDialogue
from flask import render_template, redirect, url_for

class EditServiceComponentDialogue(GenericDialogue):
    
    name = ""
    description = ""
    
    
    def create_component(self, name, description):
        
        from src.logic.monitoring.services_component_logic import ServicesComponentLogic
        
        error = ServicesComponentLogic().create_service_component(name, description)
        
        if not error:
            return ServiceComponentDialogue().ouvrir_par_redirection()
        else:
            context_data = {"destination_url": url_for('scomponent_urls.new_scomponent_handler'),
                            "name": name,
                            "description": description,
                            "update_mode":False,
                            "error":error,
                        }
            return self.ouvrir(context_data)
        
        
        
        
    def update_component(self, id_component, name, description):
        
        from src.logic.monitoring.services_component_logic import ServicesComponentLogic
        
        error = ServicesComponentLogic().update_service_component(id_component, name, description)
        if not error:
            return ServiceComponentDialogue().ouvrir_par_redirection()
        else:
            context_data = {"destination_url": url_for('scomponent_urls.update_scomponent_handler', id_component=id_component),
                            "name": name,
                            "description": description,
                            "update_mode":True,
                            "error":error,
                        }
            return self.ouvrir(context_data)
    
     
    def ouvrir(self, context_data=None):
        
        return render_template('grumos_templates/monitoring/component/form_scomponent.html', **context_data)
    
    def ouvrir_par_redirection(self, context_data=None):
        return redirect(url_for('scomponent_urls.new_scomponent_handler'))
    
    
class ServiceComponentDialogue(GenericDialogue):
    
    list_services = None
    
    def delete_component(self, id_component):
        from src.logic.monitoring.services_component_logic import ServicesComponentLogic
        ServicesComponentLogic().delete_service_component(id_component)
        return self.ouvrir_par_redirection()
            
    def update_component(self, id_component):
        
        from src.logic.monitoring.services_component_logic import ServicesComponentLogic
        context_data = {}
        component = ServicesComponentLogic().get_service_component(id_component)
        
        if component :  
            
            context_data = {"destination_url": url_for('scomponent_urls.update_scomponent_handler', id_component=component.id),
                            "name": component.name,
                            "description": component.description,
                            "update_mode":True,
                            "error":{},
                        }
        
        
        return EditServiceComponentDialogue().ouvrir(context_data)
    
    def create_component(self):
        
        context_data = {"destination_url": url_for('scomponent_urls.new_scomponent_handler'),
                        "name": "",
                        "description": "",
                        "update_mode":False,
                        "error":{},
                    }
        
        return EditServiceComponentDialogue().ouvrir(context_data)
    

    
    def ouvrir (self, context_data=None):
        from src.logic.monitoring.services_component_logic import ServicesComponentLogic
        
        data = ServicesComponentLogic().get_services()
            
        context = {
            "components": data,
            "new_scomponent_url": url_for('scomponent_urls.new_scomponent_handler'),
        }
        
        return render_template('grumos_templates/monitoring/component/list_scomponent.html', **context)        
            

    
    def ouvrir_par_redirection(self, context_data=None):
        return redirect(url_for('scomponent_urls.list_scomponent_handler'))
    