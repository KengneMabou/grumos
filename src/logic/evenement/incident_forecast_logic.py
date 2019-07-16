# coding: utf-8 
'''
Created on 17 sept. 2016

@author: kengne
'''

class IncidentForcastLogic:
    
    def correlate(self, host, metric, data):
        """
        This method correlate future event
        """
        from src.technique.evenement.sec import SimpleEvcorrWrapper
        from src.business.evenement.evenement import Incident
        import time
        from datetime import datetime
        
        inc = Incident.objects(future=True).delete()
        sec_input = open('/home/kengne/sec_assets/sec_future_event', "w+")
        try:
            for s_data in data:
                str_line = host+".hostname"+" "+metric+" "+str(int(s_data["raw_value"]))+" "+str(int(time.mktime(datetime.strptime(s_data["date"], '%Y-%m-%d %H:%M:%S').timetuple())) * 1000)
                sec_input.write(str_line+"\n")
        finally:
            sec_input.close()
        
        sec_instance = SimpleEvcorrWrapper.SimpleEvcorrWrapper(conf_path="/home/kengne/sec_assets/grumos_rules.conf")
        events = sec_instance.start("/home/kengne/sec_assets/sec_future_event")
        for e in events:
            e_part = e.split("/")
            inc = Incident(detected_by="correlation",incident_recorder="SEC (Simple Event Correlator)", state="open", description=e_part[1], gravity=e_part[2],incident_type=e_part[3],name=e_part[4], future = True).save()
            sec_instance.stop()
        return Incident.objects(future=True)
        

        
        
        
        
        
    
    