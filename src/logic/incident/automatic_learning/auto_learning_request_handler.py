# coding: utf-8 
'''
Created on 4 sept. 2016

@author: kengne
'''

from flask import Blueprint, request
from flask.views import MethodView
from src.technique.security.security import requires_session_auth, requires_permission

auto_learning_url_register = Blueprint('auto_learning_urls', __name__, template_folder='../../view/web_assets/templates/')


# request handler.
class LearningModelFittingView(MethodView):
    
    @requires_session_auth
    @requires_permission("IT_ADMIN")
    def get(self):
        from src.view.python_views.incident.auto_learning.auto_learning import AutoLearningDialogue
        return AutoLearningDialogue().model_fitting()
    
    @requires_session_auth
    @requires_permission("IT_ADMIN")
    def post(self):
        
        pass

    

class IncidentDetectionView(MethodView):

    @requires_session_auth
    @requires_permission("IT_ADMIN") 
    def get(self):
        from src.view.python_views.incident.auto_learning.auto_learning import AutoLearningDialogue
        return AutoLearningDialogue().incident_detection()
    
    @requires_session_auth
    @requires_permission("IT_ADMIN") 
    def post(self):
        pass

        
class IncidentClusteringView(MethodView):
    
    
    @requires_session_auth
    @requires_permission("IT_ADMIN") 
    def get(self, id_component):
        from src.view.python_views.incident.auto_learning.auto_learning import AutoLearningDialogue
        return AutoLearningDialogue().lauch_clustering()
    

class ListAutoLearningView(MethodView):

    @requires_session_auth
    @requires_permission("IT_ADMIN")
    def get(self):
        from src.view.python_views.system.system import GrumosDefaultDialogue
        return GrumosDefaultDialogue().auto_learning()
    
        
# Register the urls
auto_learning_url_register.add_url_rule('/console/auto_learning/', view_func=ListAutoLearningView.as_view('learning_handler'))
auto_learning_url_register.add_url_rule('/console/auto_learning/model_fitting/', view_func=LearningModelFittingView.as_view('model_fitting_handler'))
auto_learning_url_register.add_url_rule('/console/auto_learning/incident_detection/', view_func=IncidentDetectionView.as_view('incident_detection_handler'))
auto_learning_url_register.add_url_rule('/console/auto_learning/incident_clustering/', view_func=IncidentClusteringView.as_view('incident_clustering_handler'))