#!/usr/bin/python
# coding: utf-8

from mongoengine import connect, Document, StringField, IntField, ListField, ReferenceField, BooleanField, DateTimeField, Q
import sys, getopt, datetime

# plus tard améliorer l'architecture en introduisant un broker amqp vers lequel on envoit les informations nécessaire pour créer l'incident ainsi que le contexte associé. Ceci permettra d'éviter la duplication du modèle
db = connect('grumos', username='',password='',host='172.16.0.101')


metric_type_value = (('unkown', 'UNKNOW'),
                    ('software service', 'USER APPS'),
                    ('system', 'SYSTEM HOST'),
                    ('docker container', 'DOCKER CONTAINER'),
                    ('network', 'NETWORK CORE COMPONENT'),
                )

detection_choices = (('user', 'User'),
                         ('correlation', 'correlation'),
                         ('auto learning', 'Machine learning'),
                        )

gravity_choices = (('minor', 'MINOR'),
                         ('warning', 'WARNING'),
                         ('critical', 'CRITICAL'),
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


class Event(Document):
    """This class represent a grumos event. It can be a system metric, a log metric (extract from a hole raw log"""
    
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
    event_type = StringField(verbose_name="Type d'événement", max_length=255, required=False, choices=metric_type_value)
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


class IncidentContext(Document):
    name = StringField(verbose_name="Name of the context (come from the incident name)")
    events = ListField(ReferenceField(Event))

class Incident(Document):
    
	name = StringField(verbose_name="Name")
	incident_recorder = StringField(verbose_name="The name of the entity recording the incident to the system")
	description = StringField(verbose_name="Incident description")
	machines_impacted = StringField(max_length=250)
	incident_type = StringField(verbose_name="Incident type",choices = incident_type_choices)
	services_impacted = ListField(StringField(max_length=250))
	detected_by =  StringField(verbose_name="Detection Mechanism",choices = detection_choices)
	gravity = StringField(verbose_name="Incident severety",choices = gravity_choices)
	confirm = BooleanField(verbose_name="Indicate if a incident is really or only a probable incident", default=False)
	trigger_events = ListField(ReferenceField(Event)) # useful when incident result from correlation mechanism
	incident_date = DateTimeField(default = datetime.datetime.now())
	resolution_date = DateTimeField() # will be use to process MTTR
	context = ReferenceField(IncidentContext)
	state =  StringField(verbose_name="Incident state",choices = incident_state_choices, default="open")
	occurences = IntField(verbose_name="Number of occurrences", default=1) # nombre  d'occurences
	future = BooleanField(default=False)
	resolution_procedure = StringField(verbose_name="resolution procedure") # for future release
 


def main(argv):                         
	
	try:                                
		opts, args = getopt.getopt(argv, "hm:d:g:i:n:e:t:", ["help", "metrics=","description=","gravity=", "incident_type=", "name=", "equipement=", "timestamp="]) 
	except getopt.GetoptError:
		usage()
		sys.exit(2)

	arguments = {}
	for opt, arg in opts:
		if opt in ("-h", "--help"):
			usage()                     
			sys.exit()
		elif opt in ("-m", "--metrics"):
			arguments["metrics"] = arg
		elif opt in ("-d", "--description"):
			arguments["description"] = arg                
		elif opt in ("-g", "--gravity"):
			arguments["gravity"] = arg
		elif opt in ("-i", "--incident_type"):
			arguments["incident_type"] = arg
		elif opt in ("-n", "--name"):
			arguments["name"] = arg
		elif opt in ("-e", "--equipement"):
			arguments["equipement"] = arg
		elif opt in ("-t", "--timestamp"):
			arguments["timestamp"] = arg

	create_incident(arguments)


def formatMetrics(arg):

    metrics = list()
    metric_split1 = arg.split(",")
    for m in metric_split1:
        metric_split2 = m.split(":")
        metrics.append(metric_split2)
    return metrics

def create_incident(arguments):
	
	metrics = formatMetrics(arguments["metrics"])
	equip_raw = arguments["equipement"]
	equipement_part = equip_raw.split(".")
	equipement = '.'.join(equipement_part[0:len(equipement_part)-1])
	inc = Incident(detected_by="correlation",incident_recorder="SEC (Simple Event Correlator)", state="open", description=arguments["description"], gravity=arguments["gravity"],incident_type=arguments["incident_type"],name=arguments["name"], machines_impacted=equipement).save()
	
	#Incident.objects(id=inc.id).update_one(push__machines_impacted=equipement)

	event_list = Event.objects.order_by("+unix_epoch_timestamp")
	l_event = event_list[len(event_list)-1]

	for m in metrics:
		ev = Event.objects(Q(host = equipement) & Q(metric_name=m[0]) & Q(unix_epoch_timestamp=m[1])).first()
		Incident.objects(id=inc.id).update_one(push__trigger_events=ev)

	
	list_last_events = Event.objects(host = equipement, unix_epoch_timestamp = l_event.unix_epoch_timestamp) # list of events with the same timestamp as the last event for a particuler host
	i_context = IncidentContext(name=inc.name).save()
	for i_ev in list_last_events:
		IncidentContext.objects(id=i_context.id).update_one(push__events = i_ev)

	inc.context = i_context
	inc.save()	
	

def usage():
	
	print("--metric or -m: the events which causes this incident as a string in the format 'metric1:timestamp1,metric2:timestamp2'\n") 

if __name__ == "__main__":
	main(sys.argv[1:])
	sys.exit(0)

