# coding: utf-8 
'''
Created on 8 août 2016

@author: kengne
'''
from flask_script import Command

class InitAppComponent(Command):
    
    def __init__(self, func=None):
        return Command.__init__(self, func=func)
    def default_monitor_console(self):
        "This method will be use to initialize the default monitoring console aka grafana"
        from src.business.monitoring.monitoring import MonitoringConsole
        default_console_name= "Grafana"
        default_console_location = "127.0.0.1"
        default_console_port = "3000"
        default_console_path = ""
        try:
            MonitoringConsole(name = default_console_name, location = default_console_location, port = default_console_port, path = default_console_path).save()
        except:
            pass
    
    def __call__(self, app=None, *args, **kwargs):
        return Command.__call__(self, app=app, *args, **kwargs)
    
    def run(self):
        self.default_monitor_console()


class GeneralService:
    
    
    @staticmethod
    def benchmark(self, func):
        """
        Un décorateur qui affiche le temps qu'une fonction met à s'éxécuter
        """
        import time
        def wrapper(*args, **kwargs):
            t = time.clock()
            res = func(*args, **kwargs)
            print(func.__name__, time.clock()-t)
            return res
        return wrapper
    
    @staticmethod
    def console_logging(self, func):
        """
        Un décorateur qui log l'activité d'un script en console.
        
        """
        def wrapper(*args, **kwargs):
            res = func(*args, **kwargs)
            print(func.__name__, args, kwargs)
            return res
        return wrapper
    
    def journal_logging(self, func):
        """
        Un décorateur qui log l'activité d'un script en console.
        
        """
        def wrapper(*args, **kwargs):
            res = func(*args, **kwargs)
            # TODO: code du logging
            return res
        return wrapper