# coding: utf-8 
'''
Created on 26 juil. 2016

@author: kengne
'''
from src.logic.system.auth_request_handler import auth_url_register
from src.logic.application_init.staticfiles_request_handler import static_url_register
from src.logic.system.user_request_handler import user_url_register
from src.logic.monitoring.console_agg_request_handler import console_url_register
from src.logic.monitoring.monitoring_component_request_handler import hcomponent_url_register
from src.logic.evenement.metric_request_handler import event_url_register
from src.logic.etl.logstash_config_request_handler import logstash_config_url_register
from src.logic.incident.correlation.sec.sec_config_request_handler import sec_config_url_register
from src.logic.capacity_planning.capacity_forecast_request_handler import forecast_url_register
from src.logic.evenement.change_request_handler import change_url_register
from src.logic.evenement.incident_request_handler import incident_url_register
from src.logic.evenement.incident_forecast_request_handler import incident_forecast_url_register
from src.logic.monitoring.services_component_request_handler import scomponent_url_register
from src.logic.evenement.problem_request_handler import problem_url_register
from src.logic.reporting.reporting_request_handler import reporting_url_register
from src.logic.incident.automatic_learning.auto_learning_request_handler import auto_learning_url_register


def register_blueprints(app):
    # Prevents circular imports
    app.register_blueprint(auth_url_register)
    app.register_blueprint(static_url_register)
    app.register_blueprint(user_url_register)
    app.register_blueprint(console_url_register)
    app.register_blueprint(hcomponent_url_register)
    app.register_blueprint(event_url_register)
    app.register_blueprint(logstash_config_url_register)
    app.register_blueprint(sec_config_url_register)
    app.register_blueprint(forecast_url_register)
    app.register_blueprint(change_url_register)
    app.register_blueprint(incident_url_register)
    app.register_blueprint(incident_forecast_url_register)
    app.register_blueprint(scomponent_url_register)
    app.register_blueprint(problem_url_register)
    app.register_blueprint(reporting_url_register)
    app.register_blueprint(auto_learning_url_register)