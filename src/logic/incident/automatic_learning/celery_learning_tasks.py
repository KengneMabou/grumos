'''
Created on 3 nov. 2016
@author: kengne
'''
from __future__ import absolute_import
import sys, os, inspect

current_path = os.path.realpath(os.path.abspath(os.path.dirname(inspect.getfile( inspect.currentframe()))))
for i in range(1,5): # remonter les repertoires parents
    current_path = os.path.dirname(current_path)
application_dir_path = current_path
#application_dir_path = os.path.join(current_path, '') #path with the ending '/'    
sys.path.insert(0, application_dir_path)

from src.technique.mongo_engine.mongo_engine_odm import db
from celery import Celery
#

app = Celery('celery_learning_tasks', broker='amqp://guest@172.16.0.101//')
#app = Celery('celery_learning_tasks', backend='mongodb', broker='amqp://guest@localhost//', include=['tasks'])

app.config_from_object('src.logic.incident.automatic_learning.celeryconfig')
#===============================================================================
# app.conf.CELERYBEAT_SCHEDULE = {
#     'svm_classification-every-15-seconds': {
#         'task': 'celery_learning_tasks.svm_classification',
#         'schedule': timedelta(seconds=15),
#     },
# }
# 
# app.conf.CELERY_TIMEZONE = 'UTC'
#===============================================================================


@app.task(name="celery_learning_tasks.svm_classification")
def svm_classification():
    from sklearn.externals import joblib
    from src.logic.incident.automatic_learning.auto_learning_logic import svm_filename, learning_witness
    from src.logic.incident.automatic_learning.auto_learning_logic import AutoLearningLogic
    from src.logic.evenement.metric_logic import EventLogic
    import numpy as np
    
    all = AutoLearningLogic()
    context_wrapper = list()
    
    if not os.path.isfile(learning_witness):
        all.model_fitting()
           
    machines_list = EventLogic().metric_hosts()
    
    for machine in machines_list:
        context_to_classify = list()
        cur_cont = all.getCurrentContext(machine)
        cur_cont.sort(key=lambda x: x.metric_name, reverse=True)
        
        for ev in cur_cont:
            context_to_classify.append(ev.value)
        
        fp = open(learning_witness, "r")
        d_max_size = int(fp.read())
        fp.close()
        all.pad(context_to_classify, 0,d_max_size)
        
        clf = joblib.load(machine+svm_filename)
        context_wrapper.append(context_to_classify)
        res = clf.predict(np.array(context_wrapper))
        
        if res[0] == 1:
            print "The current context has been classify as an incident context"
            all.createIncident(machine, cur_cont)
        else:
            print "The current context is a normal context"
        
    

def start_worker(): 
    
    app.start(['celery','worker','-B','--loglevel=info'])
