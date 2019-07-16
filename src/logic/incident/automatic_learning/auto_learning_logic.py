# coding: utf-8 
'''
Created on 4 sept. 2016

@author: kengne
'''
import os
svm_filename = "grumos_svm_model.pkl"
learning_witness = "learning_witness"
class AutoLearningLogic:
    
    
    def incident_detection(self):
        
        from src.logic.incident.automatic_learning.celery_learning_tasks import svm_classification, start_worker
    
        if not os.path.isfile(learning_witness):
            self.model_fitting()
        
        start_worker()
        #svm_classification.delay()
        
    def model_fitting(self):
        
        self.svm_fitting()
    
    
    def svm_fitting(self):
        from sklearn import svm
        from sklearn.externals import joblib
        from src.logic.evenement.metric_logic import EventLogic
        import numpy as np
        # for training target 1 is an incident context and 0 a normal context
        
        
        machines_list = EventLogic().metric_hosts()
        
        for machine in machines_list:
            
            if os.path.isfile(machine+svm_filename):
                os.remove(machine+svm_filename)
                
            training_data_set = list()
            training_target = list()
            all_context = self.getAllContext(machine)
            #print all_context
            incident_context = self.getIncidentContext(machine)
            for context_bundle in all_context:
                context = context_bundle["context"]
                context.sort(key=lambda x: x["metric_name"], reverse=True) # sort the list of metric representing a context by "metric_name"
                data_row = list()
                
                for metric_bundle in context:
                    data_row.append(metric_bundle["value"])
                    
                if context_bundle["_id"] in incident_context:
                    training_target.append(1)
                else:
                    training_target.append(0)
                    
                training_data_set.append(data_row)    
                
            #print "mouf "+str(len(training_data_set))
            #print "moufs "+str(len(training_target))
            d_max = self.dataSetMaxLength(training_data_set)
            for ds in training_data_set: # padding short item with zero value
                if len(ds) < d_max:
                    self.pad(ds, 0, d_max)
                    
            clf = svm.SVC()
            clf.fit(np.array(training_data_set), np.array(training_target))
            joblib.dump(clf, machine+svm_filename)
        
        fp = open(learning_witness, "w")
        fp.write(str(d_max))
        fp.close()
        

    def getIncidentContext(self, machine):
        
        from src.business.evenement.evenement import Incident
        
        l_incident = Incident.objects(machines_impacted = machine)
        l_context = {}
        
        for inc in l_incident:
            #print inc.context
            if inc.context is not None:
                events = inc.context.events
                ev_zero = events[0]
                l_context[ev_zero.unix_epoch_timestamp] = events
        
        return l_context
            
    def getAllContext(self, machine):
        
        from src.business.evenement.evenement import Event
        
        result = Event.objects(host = machine).aggregate({
                "$group":{"_id":"$unix_epoch_timestamp","context":{"$push":{"metric_name":"$metric_name","value":"$value"}}}                                           
            })
        
        return list(result)
    
    def getCurrentContext(self,machine):
        
        from src.business.evenement.evenement import Event
        import datetime, time
        from mongoengine import Q
        
        current_date = datetime.datetime.now() 
        unix_date = int(time.mktime(current_date.timetuple())) * 1000
        ev = Event.objects(Q(unix_epoch_timestamp__lte = str(unix_date))).first()
        
        return list(Event.objects(Q(unix_epoch_timestamp = ev.unix_epoch_timestamp)  & Q(host = machine)))
        
    def createIncident(self, machine, context):
        from src.business.evenement.evenement import Incident, IncidentContext
        import datetime
        
        inc = Incident(name = "Incident du "+str(datetime.datetime.now()), detected_by = "auto learning", machines_impacted = machine)
        inc_context = IncidentContext(name=inc.name)
        inc_context.events = context
        inc_context.save()
        inc.save()
    
    def dataSetMaxLength(self, dataset):
        dsl = list()
        for data in dataset:
            dsl.append(len(data))
            
        return max(dsl)
    
    def pad(self, l, content, width):
        l.extend([content] * (width - len(l)))
        return l
    