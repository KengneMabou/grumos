# coding: utf-8
'''
Created on 3 nov. 2016

@author: kengne
'''
from src.view.python_views.utils.dialogue import GenericDialogue
from flask import render_template, redirect, url_for

class AutoLearningDialogue(GenericDialogue):
    
    
    def model_fitting(self):
        from src.logic.incident.automatic_learning.auto_learning_logic import AutoLearningLogic
        AutoLearningLogic().model_fitting()
        context = {
            "model_fitting_url": url_for('auto_learning_urls.model_fitting_handler'),
            "incident_detection_url":url_for('auto_learning_urls.incident_detection_handler'),
            "incident_clustering_url":url_for('auto_learning_urls.incident_clustering_handler'),
            "fitting_message": u"Apprentissage terminée avec succès, veuillez lancer la détection d'incident à présent"
        }
        
        return render_template('grumos_templates/incident/auto_learning/auto_learning.html', **context)
        
    
    def incident_detection(self):
        from src.logic.incident.automatic_learning.auto_learning_logic import AutoLearningLogic
        AutoLearningLogic().incident_detection()
    
    def ouvrir (self, context_data=None):
            
        context = {
            "model_fitting_url": url_for('auto_learning_urls.model_fitting_handler'),
            "incident_detection_url":url_for('auto_learning_urls.incident_detection_handler'),
            "incident_clustering_url":url_for('auto_learning_urls.incident_clustering_handler'),
        }
        
        return render_template('grumos_templates/incident/auto_learning/auto_learning.html', **context)        
            

    
    def ouvrir_par_redirection(self, context_data=None):
        return redirect(url_for('auto_learning_urls.learning_handler'))
