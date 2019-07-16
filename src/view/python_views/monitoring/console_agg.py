# coding: utf-8 
'''
Created on 3 sept. 2016

@author: kengne
'''

from src.view.python_views.utils.dialogue import GenericDialogue
from flask import render_template, redirect, url_for

class EditConsoleDialogue(GenericDialogue):
    
    name = ""
    location = ""
    port = ""
    path = ""
    
    def create_console(self, name, location, port, path):
        
        from src.logic.monitoring.console_agg_logic import ConsoleAggLogic
        
        error = ConsoleAggLogic().create_console(name, location, port, path)
        
        if not error:
            return ConsoleAggDialogue().ouvrir_par_redirection()
        else:
            context_data = {"destination_url": url_for('console_agg_urls.new_console_handler'),
                            "name": name,
                            "location": location,
                            "port" : port,
                            "path" : path,
                            "update_mode":False,
                            "error":error,
                        }
            return self.ouvrir(context_data) 
        
        
        
        
    def update_console(self, id_console, name, location, port, path):
        
        from src.logic.monitoring.console_agg_logic import ConsoleAggLogic
        
        error = ConsoleAggLogic().update_console(id_console, name, location, port, path)
        if not error:
            return ConsoleAggDialogue().ouvrir_par_redirection()
        else:
            context_data = {"destination_url": url_for('console_agg_urls.update_console_handler', id_console=id_console),
                            "name": name,
                            "location": location,
                            "port" : port,
                            "path" : path,
                            "update_mode":True,
                            "error":error,
                        }
            return self.ouvrir(context_data)
    
     
    def ouvrir(self, context_data=None):
        
        return render_template('grumos_templates/monitoring/console/form_console.html', **context_data)
    
    def ouvrir_par_redirection(self, context_data=None):
        return redirect(url_for('console_agg_urls.new_console_handler'))
    
    
class ConsoleAggDialogue(GenericDialogue):
    
    list_consoles = None
    
    def delete_console(self, id_console):
        from src.logic.monitoring.console_agg_logic import ConsoleAggLogic
        ConsoleAggLogic().delete_console(id_console)
        return self.ouvrir_par_redirection()
            
    def update_console(self, id_console):
        
        from src.logic.monitoring.console_agg_logic import ConsoleAggLogic
        context_data = {}
        console = ConsoleAggLogic().get_console(id_console)
        
        if console : 
            
            context_data = {"destination_url": url_for('console_agg_urls.update_console_handler', id_console=console.id),
                            "name": console.name,
                            "location": console.location,
                            "port" : console.port,
                            "path" : console.path,
                            "update_mode":True,
                            "error":{},
                        }
        
        
        return EditConsoleDialogue().ouvrir(context_data)
    
    def create_console(self):
        
        context_data = {"destination_url": url_for('console_agg_urls.new_console_handler'),
                        "name": "",
                        "location": "",
                        "port" : "",
                        "path" : "",
                        "update_mode":False,
                        "error":{},
                    }
        
        return EditConsoleDialogue().ouvrir(context_data)
    
    def view_consoles(self):
    
        from src.logic.monitoring.console_agg_logic import ConsoleAggLogic
        #from flask import make_response
        
        data = ConsoleAggLogic().list_consoles()
        
        for console in data:
            console.full_url = 'http://'+console.location+":"+console.port+"/"+console.path
       
        context = {
                "consoles": data,
            }
        
        #r = make_response(render_template('grumos_templates/monitoring/console/test.html', **context))
        #r.headers.add('Access-Control-Allow-Origin:', "192.168.1.183:3000")
        #return r
        return render_template('grumos_templates/monitoring/console/view_console.html', **context)  
    
    def ouvrir (self, context_data=None):
        from src.logic.monitoring.console_agg_logic import ConsoleAggLogic
        
        data = ConsoleAggLogic().list_consoles()
        
        context = {
            "consoles": data,
            "new_console_url": url_for('console_agg_urls.new_console_handler'),
            "view_console_url": url_for('console_agg_urls.view_console_handler'),
        }
        
        return render_template('grumos_templates/monitoring/console/list_console.html', **context)        
            

    
    def ouvrir_par_redirection(self, context_data=None):
        return redirect(url_for('console_agg_urls.list_console_handler'))
