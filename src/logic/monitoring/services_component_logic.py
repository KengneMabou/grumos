# coding: utf-8 
'''
Created on 4 sept. 2016

@author: kengne
'''
from mongoengine import Q

class ServicesComponentLogic:
    
        
    def list_services(self):
        
        from src.business.monitoring.monitoring import ServiceComponent
        
        l_serv = ServiceComponent.objects.distinct("name")
        
        return l_serv
    
    def get_services(self):
        
        from src.business.monitoring.monitoring import ServiceComponent
        
        services = ServiceComponent.objects
        
        return services
    
    def delete_service_component(self, id_component):
        """method for deleting hardware component"""
        from src.business.monitoring.monitoring import ServiceComponent
        
        error = None
        component = ServiceComponent.objects(id=id_component).first()
        
        if component :
            component.delete()
        
        return error

    def get_service_component(self, id_component):
        """method for getting a single hardware component given his id"""
        from src.business.monitoring.monitoring import ServiceComponent
        
        component = ServiceComponent.objects(id=id_component).first()
        
        return component
              
    def list_service_component(self):
        from src.business.monitoring.monitoring import ServiceComponent
        
        components = ServiceComponent.objects.all()
        
        return components


    def update_service_component(self, id_component, name, description):
        """
            Method for updating infos about a hardware component to monitor
        """
        from src.business.monitoring.monitoring import ServiceComponent
        
        error = self.validate_form_create(name, description)
        
        if not error:
            component =  ServiceComponent.objects(id=id_component).first()
            component.name = name
            component.description = description
            component.save()
        return error
    
    def create_service_component(self,_name, _description):
        """This method is for registring a new hardware component to monitor"""
        from src.business.monitoring.monitoring import ServiceComponent
        error = self.validate_form_create(_name, _description)
        if not error:
            ServiceComponent(name = _name, description = _description).save()
        
        return error
            
    def validate_form_create(self, _name, _description):
        
        """
        method for validating input data during hardware component creation process
        """
        from src.business.monitoring.monitoring import ServiceComponent
        
        error = None
        
            
        component =ServiceComponent.objects(name=_name).first()
        
        if component:
            if not error: 
                error = {}
            error["name_exist_error"] = u"Ce nom existe déjà"
            
        if _name == "":
            if not error: 
                error = {}
            error["name_empty_error"] = u"Le nom du service est obligatoire"
               
        
        return error
    
    def validate_form_update(self, id_component, _name, _description):
        
        """
        method for validating input data during hard component udpate process
        """
        from src.business.monitoring.monitoring import ServiceComponent

        error = None
        
            
        component =ServiceComponent.objects(name=_name).first()
        
        if component and str(component.id) != str(id_component):
            if not error: 
                error = {}
            error["name_exist_error"] = u"Ce nom existe déjà"
            
        if _name == "":
            if not error: 
                error = {}
            error["name_empty_error"] = u"Le nom du service est obligatoire"
               
        
                 
        return error
