# -*- coding: utf-8 -*
'''
Created on 26 juil. 2016

@author: kengne
'''

from src.view.python_views.utils.dialogue import GenericDialogue
from src.logic.system.auth_logic import AuthAppLogic
from flask import render_template, session, redirect, url_for, flash
from src.technique.application_init.settings_vars import user_profiles, session_attrs, list_profiles

class AuthDialogue(GenericDialogue):
    
    login = ""
    password = ""
    result = ""
    
    def validerFacteurAuth(self, login, password):
        if AuthAppLogic().valider(login, password):
            flash(u'connexion réussie')
            return GrumosDefaultDialogue().ouvrir_par_redirection()
        else:
            self.result = u"login ou mot de passe incorrect"
            return self.ouvrir(self.result)
            
            
            
        
    def ouvrir(self, context_data=None):
        return render_template('admin_lte/pages/examples/login.html', auth_error = context_data)
        #return render_template('admin_lte/index.html', auth_error = context_data)
    
    def ouvrir_par_redirection(self, context_data=None):
        return redirect(url_for('auth_urls.login_handler'))
    


class PermissionDialogue(GenericDialogue):
                        
    def ouvrir(self, context_data=None):
        return render_template('grumos_templates/system/permission.html')
    

class EditUserDialogue(GenericDialogue):
    
    name = ""
    surname = ""
    email = ""
    login = ""
    password = ""
    profile = ""
    
   
    
    def create_user(self, name, surname, email, login, password, passwordBis, profile):
        
        from src.logic.system.user_logic import UserMgtLogic
        
        error = UserMgtLogic().create_user(name, surname, email, login, password, passwordBis, profile)
        
        if not error:
            return UsersDialogue().ouvrir_par_redirection()
        else:
            context_data = {"destination_url": url_for('user_urls.new_user_handler'),
                            "name": name,
                            "surname": surname,
                            "email" : email,
                            "login" : login,
                            "password" : password,
                            "profile" : profile,
                            "list_profiles":list_profiles,
                            "update_mode":False,
                            "error":error,
                        }
            return self.ouvrir(context_data) 
        
        
        
        
    def update_user(self, id_user, name, surname, email, login, password, passwordBis, profile):
        
        from src.logic.system.user_logic import UserMgtLogic
        
        error = UserMgtLogic().update_user(id_user, name, surname, email, login, password, passwordBis, profile)    
        if not error:
            return UsersDialogue().ouvrir_par_redirection()
        else:
            context_data = {"destination_url": url_for('user_urls.update_user_handler', id_user=id_user),
                            "name": name,
                            "surname": surname,
                            "email" : email,
                            "login" : login,
                            "password" : password,
                            "profile" : profile,
                            "list_profiles":list_profiles,
                            "update_mode":True,
                            "error":error,
                        }
            return self.ouvrir(context_data)
    
    def update_user_profile(self, id_user, name, surname, email, login, password, passwordBis):
        
        """Méthode pour mettre à jour le profil utilisateur"""
        
        from src.logic.system.user_logic import UserMgtLogic
        
        error = UserMgtLogic().update_user_profile(id_user, name, surname, email, login, password, passwordBis)    
        if not error:
            return GrumosDefaultDialogue().root()
        else:
            context_data = {"destination_url": url_for('user_urls.profile_handler', id_user=id_user),
                            "name": name,
                            "surname": surname,
                            "email" : email,
                            "login" : login,
                            "password" : password,
                            "profile" : None ,
                            "update_mode":True,
                            "error":error,
                        }
            return self.ouvrir(context_data)  
        
    def ouvrir(self, context_data=None):
        return render_template('grumos_templates/system/user/form_user.html', **context_data)
        #return render_template('admin_lte/index.html', auth_error = context_data)
    
    def ouvrir_par_redirection(self, context_data=None):
        return redirect(url_for('auth_urls.login_handler'))
    
    
class UsersDialogue(GenericDialogue):
    
    list_users = None
    
    def delete_user(self, id_user):
        from src.logic.system.user_logic import UserMgtLogic
        UserMgtLogic().delete_user(id_user)
        return self.ouvrir_par_redirection()
            
    def update_user(self, id_user):
        
        from src.logic.system.user_logic import UserMgtLogic
        context_data = {}
        user = UserMgtLogic().get_user(id_user)
        
        if user : 
            
            context_data = {"destination_url": url_for('user_urls.update_user_handler', id_user=user.id),
                            "name": user.name,
                            "surname": user.surname,
                            "email" : user.email,
                            "login" : user.login,
                            "password" : user.password,
                            "profile" : user.profile,
                            "list_profiles":list_profiles,
                            "update_mode":True,
                            "error":{},
                        }
        
        
        return EditUserDialogue().ouvrir(context_data)
    
    def create_user(self):
        
        
        context_data = {"destination_url": url_for('user_urls.new_user_handler'),
                        "name": "",
                        "surname": "",
                        "email" : "",
                        "login" : "",
                        "password" : "",
                        "profile" : "",
                        "list_profiles":list_profiles,
                        "update_mode":False,
                        "error":{},
                    }
        
        return EditUserDialogue().ouvrir(context_data)
    
    def ouvrir (self, context_data=None):
        from src.logic.system.user_logic import UserMgtLogic
        
        data = UserMgtLogic().list_users()
        
        context = {
            "users": data,
            "new_user_url": url_for('user_urls.new_user_handler'),
        }
        
        return render_template('grumos_templates/system/user/list_user.html', **context)        
            

    
    def ouvrir_par_redirection(self, context_data=None):
        return redirect(url_for('user_urls.list_user_handler'))
    

    
class GrumosDefaultDialogue(GenericDialogue):
    
            
        
    def ouvrir(self, context_data=None):
        
        if session.get(session_attrs.get('profile_attr')) == user_profiles.get('manager'):
            
            return render_template('admin_lte/index.html', auth_error = context_data)
       
        
        elif session.get(session_attrs.get('profile_attr')) == user_profiles.get('admin'):
            
            return render_template('admin_lte/index.html', auth_error = context_data)
        
        elif session.get(session_attrs.get('profile_attr')) == user_profiles.get('bpo'):
            
            return render_template('admin_lte/index.html', auth_error = context_data)
        
        else:
            
            return render_template('admin_lte/index.html', auth_error = context_data)
    
    
    def ouvrir_par_redirection(self):
        
        return redirect(url_for('console_agg_urls.view_console_handler'))
            
        
    
    def controlerChamps(self):
        pass
    
    def login (self):
        return AuthDialogue().ouvrir()
    
    def root (self):
        return AuthAppLogic().root()
    
    def logout (self):
        AuthAppLogic().logout()
        flash(u'déconnexion réussie')
        return AuthDialogue().ouvrir_par_redirection()
    
    def profile (self, id_user):
        
        from src.logic.system.user_logic import UserMgtLogic
        context_data = {}
        user = UserMgtLogic().get_user(id_user)
        
        if user : 
            
            context_data = {"destination_url": url_for('user_urls.profile_handler', id_user=user.id),
                            "name": user.name,
                            "surname": user.surname,
                            "email" : user.email,
                            "login" : user.login,
                            "password" : user.password,
                            "profile" : None,
                            "update_mode":True,
                            "error":{},
                        }
        
        
        return EditUserDialogue().ouvrir(context_data)
    
    def users (self):
        
        return UsersDialogue().ouvrir()
    
    def console_agg (self):
        from src.view.python_views.monitoring.console_agg import ConsoleAggDialogue
        return ConsoleAggDialogue().ouvrir()
    
    def h_components (self):
        from src.view.python_views.monitoring.hard_component import HardComponentDialogue
        return HardComponentDialogue().ouvrir()
    
    def events (self, number_items, event_type, page):
        from src.view.python_views.evenement.event import EventDialogue
        return EventDialogue().ouvrir(number_items, event_type, page)
    
    def logstash_config(self):
        from src.view.python_views.etl.logstash_config import LogstashConfigPoolDialogue
        return LogstashConfigPoolDialogue().ouvrir()
    
    def sec_config(self):
        from src.view.python_views.incident.correlation.sec.sec_config import SecConfigPoolDialogue
        return SecConfigPoolDialogue().ouvrir()
    
    def capacity_forecast(self):
        from src.view.python_views.capacity_planning.capacity_forecast import CapacityForecastDialogue
        return CapacityForecastDialogue().ouvrir()
    
    def changes (self, number_items, change_type, page):
        from src.view.python_views.evenement.change import ChangeDialogue
        return ChangeDialogue().ouvrir(number_items, change_type, page)
    
    def incidents (self, number_items, incident_type, page):
        from src.view.python_views.evenement.incident import IncidentDialogue
        return IncidentDialogue().ouvrir(number_items, incident_type, page)
    
    def problems (self, number_items, problem_type, page):
        from src.view.python_views.evenement.problem import ProblemDialogue
        return ProblemDialogue().ouvrir(number_items, problem_type, page)
    
    def incidents_forecast(self):
        from src.view.python_views.evenement.incident_forecast import IncidentForecastDialogue
        return IncidentForecastDialogue().ouvrir()
    
    def s_components (self):
        from src.view.python_views.monitoring.service_component import ServiceComponentDialogue
        return ServiceComponentDialogue().ouvrir()
    
    def report (self):
        from src.view.python_views.reporting.reporting import ReportingComponentDialogue
        return ReportingComponentDialogue().ouvrir()
    
    def auto_learning (self):
        from src.view.python_views.incident.auto_learning.auto_learning import AutoLearningDialogue
        return AutoLearningDialogue().ouvrir()
        
    
    
             
    
   
    
        
    
        
        
    