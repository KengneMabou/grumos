'''
Created on 12 sept. 2016

@author: kengne
'''

class EventLogic:
    
    
    console = None
    

    def delete_event(self, id_event):
        from src.business.evenement.evenement import Event
        
        error = None
        evt = Event.objects(id=id_event).first()
        
        if evt :
            evt.delete()
        
        return error
    

    def get_event(self, id_event):
        from src.business.evenement.evenement import Event
        
        evt = Event.objects(id=id_event).first()
        
        return evt
          
    def list_events(self, number_items = 0, event_type = None, page = 1):
        from src.business.evenement.evenement import Event
        import datetime
        events = {}
        
        number_items = int(number_items)
        page = int(page) 
        
        if event_type is None:
            events = Event.objects
        else:
            events = Event.objects(event_type=event_type)
            
        if number_items > 0:
            maxi = page*number_items
            mini = page*number_items - number_items
            events = events[mini:maxi]
            
        for evt in events:
            
            evt.date = datetime.datetime.fromtimestamp(int(int(evt.unix_epoch_timestamp)/1000)).strftime('%Y-%m-%d %H:%M:%S')
 
            
        return events
    
    def naive_list_events(self):
        from src.business.evenement.evenement import Event
        return Event.objects.all()

    def metric_hosts(self):
        from src.business.evenement.evenement import Event
        l_hosts = Event.objects.distinct("host")
        return l_hosts