# coding: utf-8 
'''
Created on 12 sept. 2016

@author: kengne
'''

from mongoengine import Document, IntField, StringField, BooleanField, ListField, DateTimeField, ReferenceField
import datetime
from src.business.system.utilisateur import User

metric_type_value = (('unkown', 'UNKNOW'),
                    ('software service', 'USER APPS'),
                    ('system', 'SYSTEM HOST'),
                    ('docker container', 'DOCKER CONTAINER'),
                    ('network', 'NETWORK CORE COMPONENT'),
                )

change_type_choices = (('configuration change', 'configuration change'),
                    ('service deployment', 'service deployment'),
                )



class Event(Document):
    """This class represent a grumos metric. It can be a system metric, a log metric (extract from a hole raw log"""
    
    host = StringField(verbose_name="Nom d'hôte de machine ou d'un utilisateur grumos", max_length=255, required=True)
    sourceIPAddr = StringField(verbose_name="Adresse IP source", required=False)
    destinationHostname = StringField(verbose_name="Nom de l'hote de destination", required=False)
    destinationIPAddr = StringField(verbose_name="Adresse IP de l'hote de destination", required=False)
    plugin = StringField(verbose_name="Famille des composant monitoré", max_length=255, required=True)
    plugin_instance = StringField(verbose_name="Composant concret", max_length=255, required=False)
    type_instance = StringField(verbose_name="Point d'observation", max_length=255, required=False)
    value = StringField(verbose_name="Valeur ou description de l'événement", required=False)
    unix_epoch_timestamp = StringField(verbose_name="Timestamp", max_length=255, required=False)
    metric_instance = StringField(verbose_name="Métrique", max_length=255, required=False)
    event_type = StringField(verbose_name="Type de métriques", max_length=255, required=False, choices=metric_type_value)
    metric_name = StringField(verbose_name="Nom complet de la métrique", max_length=255, required=False)
    correlation_msg = StringField(verbose_name="Message pour la corrélation", required=False)
    description = StringField(verbose_name="Description de l'événement",required=False)
    extra_data = StringField(verbose_name="Extra data")
    correlate =  BooleanField(verbose_name="Whether or not use this event in correlation")
    date = ""# don't touch 
    meta = {
        'collection': 'perf_data',
        'strict':False,
        'ordering': ['-unix_epoch_timestamp'],
    }
    
class Change(Document):
    """This class represent a change event"""
   
    notifier = ReferenceField(User)
    name = StringField(verbose_name="Nom du changement", max_length=255, required=True)
    description = StringField(verbose_name="Description de l'événement",required=False)
    machines_impacted = ListField(StringField(max_length=250))
    change_type = StringField(verbose_name="Change type",choices = change_type_choices)
    services_impacted = ListField(StringField(max_length=250))
    change_date = DateTimeField(default = datetime.datetime.now()) # date at which the change has occured
    write_date = DateTimeField(default = datetime.datetime.now())
    
    
    

detection_choices = (('user', 'User'),
                         ('correlation', 'correlation'),
                         ('auto learning', 'Machine learning'),
                        )

gravity_choices = (('minor', 'Minor'),
                         ('warning', 'Warning'),
                         ('critical', 'Critical'),
                        )

incident_state_choices = (('open', 'Ouvert'),
                         ('resolved', 'Résolu'),
                         ('non resolved', 'Non résolu'),
                        )

incident_type_choices = (('network', 'network core component'),
                         ('system', ' end system component'),
                         ('software service', 'software service unavailable'),
                         ('docker container', 'docker container'),
                        )



class IncidentContext(Document):
    name = StringField(verbose_name="Name of the context (come from the incident name)")
    events = ListField(ReferenceField(Event))
   
   
class Incident(Document): #Dans le sens d'alerte
    
    name = StringField(verbose_name="Name")
    incident_recorder = StringField(verbose_name="The name of the entity recording the incident to the system")
    description = StringField(verbose_name="Incident description")
    machines_impacted = StringField(max_length=250)
    incident_type = StringField(verbose_name="Incident type",choices = incident_type_choices)
    services_impacted = ListField(StringField(max_length=250))
    detected_by =  StringField(verbose_name="Detection Mechanism",choices = detection_choices, default="correlation")
    gravity = StringField(verbose_name="Incident severety",choices = gravity_choices, default="warning")
    confirm = BooleanField(verbose_name="Indicate if a incident is really or only a probable incident", default=False)
    trigger_events = ListField(ReferenceField(Event)) # useful when incident result from correlation mechanism
    incident_date = DateTimeField(default = datetime.datetime.now())
    resolution_date = DateTimeField() # will be use to process MTTR
    context = ReferenceField(IncidentContext)
    state =  StringField(verbose_name="Incident state",choices = incident_state_choices, default="open")
    occurences = IntField(verbose_name="Number of occurrences", default=1) # nombre  d'occurences
    future = BooleanField(default=False)
    resolution_procedure = StringField(verbose_name="resolution procedure") # for future release
    
    meta = {
        'strict':False,
    }

problem_type_choices = (('hardware', 'Hardware'),
                         ('network', 'network core component'),
                         ('system', ' end system component'),
                         ('software service', 'software service unavailable'),
                         ('docker container', 'docker container'),
                        )
priority_choices = (('low', 'Low'),
                         ('medium', 'medium'),
                         ('high', 'High'),
                        )

class Problem(Document):
    
    name = StringField(verbose_name="Name")
    problem_recorder = StringField(verbose_name="The name of the entity recording the problem to the system")
    description = StringField(verbose_name="Problem description")
    machines_impacted = ListField(StringField(max_length=250))
    problem_type = StringField(verbose_name="Problem type",choices = problem_type_choices)
    services_impacted = ListField(StringField(max_length=250))
    priority = StringField(verbose_name="Problem priority",choices = priority_choices)
    associated_incident = ListField(ReferenceField(Incident)) # for future release
    problem_date = DateTimeField(default = datetime.datetime.now())
    resolution_date = DateTimeField() # will be use to process MTTR
    state =  StringField(verbose_name="Problem state",choices = incident_state_choices, default="open")
    occurences = IntField(verbose_name="Number of occurrences", default=1) # nombre  d'occurences
    future = BooleanField(default=False)
    confirm = BooleanField(default=False)
    resolution_procedure = StringField(verbose_name="resolution procedure") # for future release
    