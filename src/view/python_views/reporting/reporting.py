'''
Created on 26 oct. 2016

@author: kengne
'''
from src.view.python_views.utils.dialogue import GenericDialogue
from flask import render_template, redirect, url_for

class ReportingComponentDialogue(GenericDialogue):
    
    
    def incident_report(self):
        
        from src.logic.reporting.reporting_logic import ReportingLogic
        
        data = ReportingLogic().get_incident_report_data()
            
        context = {
            "report_data": data,
        }
        
        return render_template('grumos_templates/reporting/incident_reporting.html', **context)
            
    def problem_report(self):
        
        from src.logic.reporting.reporting_logic import ReportingLogic
        
        data = ReportingLogic().get_problem_report_data()
            
        context = {
            "report_data": data,
        }
        
        return render_template('grumos_templates/reporting/problem_reporting.html', **context)
    
    def change_report(self):
        
        from src.logic.reporting.reporting_logic import ReportingLogic
        
        data = ReportingLogic().get_change_report_data()
            
        context = {
            "report_data": data,
        }
        
        return render_template('grumos_templates/reporting/change_reporting.html', **context)
    
    
    
    def ouvrir (self, context_data=None):
        from src.logic.reporting.reporting_logic import ReportingLogic
        
        data = ReportingLogic().get_consoles()
            
        context = {
            "consoles": data,
        }
        
        return render_template('grumos_templates/reporting/view_reporting_consoles.html', **context)        
            

    
    def ouvrir_par_redirection(self, context_data=None):
        return redirect(url_for('reporting_urls.reporting_consoles_handler'))
    