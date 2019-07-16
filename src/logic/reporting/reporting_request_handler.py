# coding: utf-8 
'''
Created on 12 sept. 2016

@author: kengne
'''

from flask import Blueprint, request
from flask.views import MethodView
from src.technique.security.security import requires_session_auth, requires_permission

reporting_url_register = Blueprint('reporting_urls', __name__, template_folder='../../view/web_assets/templates/')


class ReportingConsolesView(MethodView):
    
    @requires_session_auth
    @requires_permission("IT_ADMIN")
    def get(self):
        from src.view.python_views.system.system import GrumosDefaultDialogue
        return GrumosDefaultDialogue().report()

class IncidentReportView(MethodView):
    
    @requires_session_auth
    @requires_permission("IT_ADMIN")
    def get(self):
        from src.view.python_views.reporting.reporting import ReportingComponentDialogue
        return ReportingComponentDialogue().incident_report()
    

class ProblemReportView(MethodView):
    
    @requires_session_auth
    @requires_permission("IT_ADMIN")
    def get(self):
        from src.view.python_views.reporting.reporting import ReportingComponentDialogue
        return ReportingComponentDialogue().problem_report()

class ChangeReportView(MethodView):
    
    @requires_session_auth
    @requires_permission("IT_ADMIN")
    def get(self):
        from src.view.python_views.reporting.reporting import ReportingComponentDialogue
        return ReportingComponentDialogue().change_report()
    
   
# Register the urls

reporting_url_register.add_url_rule('/console/reportings/', view_func=ReportingConsolesView.as_view('reporting_consoles_handler'))
reporting_url_register.add_url_rule('/console/reportings/incidents/', view_func=IncidentReportView.as_view('incidents_report_handler'))
reporting_url_register.add_url_rule('/console/reportings/problems/', view_func=ProblemReportView.as_view('problems_report_handler'))
reporting_url_register.add_url_rule('/console/reportings/changes/', view_func=ChangeReportView.as_view('changes_report_handler'))
