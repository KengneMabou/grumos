# coding: utf-8 
'''
Created on 12 sept. 2016

@author: kengne
'''

class ChangeLogic:
    
    
    change = None

    
    def filter_changes(self, number_items = 0, change_type = None, page = 1):
        
        from src.business.evenement.evenement import Change
        
        changes = {}
        
        number_items = int(number_items)
        page = int(page) 
        
        if change_type is None:
            changes = Change.objects
        else:
            changes = Change.objects(change_type=change_type)
            
        if number_items > 0:
            maxi = page*number_items
            mini = page*number_items - number_items
            changes = changes[mini:maxi]
            
        return changes

    def delete_change(self, id_change):
        from src.business.evenement.evenement import Change
        
        error = None
        change = Change.objects(id=id_change).first()
        
        if change :
            change.delete()
        
        return error
    

    def get_change(self, id_change):
        from src.business.evenement.evenement import Change
        
        ch = Change.objects(id=id_change).first()
        
        return ch
          
    def list_changes(self):
        from src.business.evenement.evenement import Change
        
        changes = Change.objects.all()
        
        return changes


    def update_change(self, id_change, name, description, machines_impacted, change_type, services_impacted, change_date):
        """
            Method for updating infos about a change
        """
        from src.business.evenement.evenement import Change
        
        error = self.validate_form_update(id_change, name, description, machines_impacted, change_type, services_impacted, change_date)
        
        if not error:
            change =  Change.objects(id=id_change).first()
            change.name = name
            change.description = description
            change.machines_impacted =machines_impacted
            change.change_type = change_type
            change.services_impacted = services_impacted
            change.change_date = change_date
            change.save()
        return error
    
    def create_change(self,name, description, machines_impacted, change_type, services_impacted, change_date):
        """This method is for registring a new change"""
        from src.business.evenement.evenement import Change
        from src.business.system.utilisateur import User
        from flask import session
        from src.technique.application_init.settings_vars import session_attrs
        user = User.objects(login = session[session_attrs.get('username_attr')]).first()
        error = self.validate_form_create(name, description, machines_impacted, change_type, services_impacted, change_date)
        if not error:
            Change(notifier = user, name = name, description = description, machines_impacted = machines_impacted, change_type = change_type, services_impacted = services_impacted, change_date = change_date).save()
        
        return error
        
    def validate_form_create(self, name, description, machines_impacted, change_type, services_impacted, change_date):
        
        """
        method for validating input data during change creation process
        """

        
        error = None
            
        if name == "":
            if not error: 
                error = {}
            error["name_empty_error"] = u"Le nom duchangement est obligatoire"
               
            
        if change_date == "": #TODO , we are also going to put a regex-based control to see if the date has the correct format
            if not error: 
                error = {}
            error["change_date_empty _error"] = u"la date du changement est obligatoire"
            
            
            
        return error
    
    def validate_form_update(self, id_change, name, description, machines_impacted, change_type, services_impacted, change_date):
        
        """
        method for validating input data during change udpate process
        """
        
        error = None
        
            
        if name == "":
            if not error: 
                error = {}
            error["name_empty_error"] = u"Le nom du changement est obligatoire"
               
            
        if change_date == "": #TODO , we are also going to put a regex-based control to see if the date has the correct format
            if not error: 
                error = {}
            error["change_date_empty _error"] = u"la date du changement est obligatoire"
            
            
        return error
    
