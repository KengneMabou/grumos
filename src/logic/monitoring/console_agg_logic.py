# coding: utf-8 
'''
Created on 4 août 2016

@author: kengne
'''
        
class ConsoleAggLogic:
    
    
    console = None
    

    def delete_console(self, id_console):
        from src.business.monitoring.monitoring import MonitoringConsole
        
        error = None
        console = MonitoringConsole.objects(id=id_console).first()
        
        if console :
            console.delete()
        
        return error
    

    def get_console(self, id_console):
        from src.business.monitoring.monitoring import MonitoringConsole
        
        console = MonitoringConsole.objects(id=id_console).first()
        
        return console
          
    def list_consoles(self):
        from src.business.monitoring.monitoring import MonitoringConsole
        
        consoles = MonitoringConsole.objects.all()
        
        return consoles


    def update_console(self, id_console, name, location, port, path):
        """
            Method for updating infos about a monitoring console
        """
        from src.business.monitoring.monitoring import MonitoringConsole
        
       
        error = self.validate_form_update(id_console, name, location, port, path)
        
        if not error:
            console =  MonitoringConsole.objects(id=id_console).first()
            console.name = name
            console.location = location
            console.port = port
            console.path = path
            console.save()
        return error
    
    def create_console(self,_name, _location, _port, _path):
        """This method is for registring a new monitoring console"""
        from src.business.monitoring.monitoring import MonitoringConsole
        error = self.validate_form_create(_name, _location, _port, _path)
        if not error:
            MonitoringConsole(name = _name, location = _location, port=_port, path = _path).save()
        
        return error
        
    def validate_form_create(self, _name, _location, _port, _path):
        
        """
        method for validating input data during console creation process
        """
        from src.business.monitoring.monitoring import MonitoringConsole
        
        error = None
        
        try:
            _port = int(_port)
        except ValueError:
            _port = None
            
        console = MonitoringConsole.objects(name=_name).first()
        
        if console:
            if not error: 
                error = {}
            error["name_exist_error"] = u"Ce nom existe déjà"
            
        if _name == "":
            if not error: 
                error = {}
            error["name_empty_error"] = u"Le nom de la console est obligatoire"
               
        if  not isinstance(_port, int) and not isinstance(_port, long):
            if not error: 
                error = {}
            error["port_error"] = u"Le numéro de port n'est pas valide; doit être un entier compris entre 0 et 65000"
            
        if _location == "":
            if not error: 
                error = {}
            error["location_empty _error"] = u"l'adresse de la console de monitoring est obligatoire"
            
            
        return error
    
    def validate_form_update(self, id_console, _name, _location, _port, _path):
        
        """
        method for validating input data during console udpate process
        """
        from src.business.monitoring.monitoring import MonitoringConsole
        
        error = None
        
        try:
            _port = int(_port)
        except ValueError:
            _port = None
            
        console = MonitoringConsole.objects(name=_name).first()
        
            
        if console and str(console.id) != str(id_console):
            if not error: 
                error = {}
            error["name_exist_error"] = u"Ce nom existe déjà"
            
        if _name == "":
            if not error: 
                error = {}
            error["name_empty_error"] = u"Le nom de la console est obligatoire"
               
        if  not isinstance(_port, int) and not isinstance(_port, long):
            if not error: 
                error = {}
            error["port_error"] = u"Le numéro de port n'est pas valide; doit être un entier compris entre 0 et 65000"
            
        if _location == "":
            if not error: 
                error = {}
            error["location_empty _error"] = u"l'adresse de la console de monitoring est obligatoire"
            
            
        return error
    
    
            
        
