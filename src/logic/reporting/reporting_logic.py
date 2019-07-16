# coding: utf-8 
'''
Created on 12 sept. 2016

@author: kengne
'''

class ReportingLogic:
    
    
    
    def get_consoles(self):
        
        from flask import url_for
        
        consoles = list()
        
        consoles.append({"name":"Incidents","full_url":url_for('reporting_urls.incidents_report_handler')})
        consoles.append({"name":"Problems","full_url":url_for('reporting_urls.problems_report_handler')})
        consoles.append({"name":"Changes","full_url":url_for('reporting_urls.changes_report_handler')})
            
        return consoles
    
    def get_change_report_data(self):
        
        from src.business.evenement.evenement import Change
        
        report = {}
        
        cpt_color = 0
        
        colors_pool = ["#bca349","#2081c1","#d0743c","#69a5f9","#98a9c5", "#e4a049"]
        
        i_queryset = Change.objects
           
        mtbc, mtbc_hr = self.compute_change_mtbc()
        
        report["changes_length"] =  len(i_queryset)
        report["changes_mtbc"] =  mtbc_hr
                    
        l_change_type = list()
        for typ in self.list_change_type():
            
            change_by_type = {}
            change_by_type["label"] = typ
            change_by_type["value"] = len(self.changes_by_type(typ))
            change_by_type["color"] = colors_pool[cpt_color]
            l_change_type.append(change_by_type)
            cpt_color = cpt_color +1
            if cpt_color == 6:
                cpt_color = 0
                

        report["change_by_type"] = l_change_type
        
        return report
    
    def get_incident_report_data(self):
        
        from src.business.evenement.evenement import Incident
        
        report = {}
        
        cpt_color = 0
        
        colors_pool = ["#bca349","#2081c1","#d0743c","#69a5f9","#98a9c5", "#e4a049"]
        
        i_queryset = Incident.objects
           
        mttr, mttr_hr  = self.compute_incident_mttr()
        mtbf, mtbf_hr = self.compute_incident_mtbf()
        
        availability = 0
        if mttr+mtbf != 0:
            availability = mtbf/(mttr+mtbf)
            
        maintanability = 0
        if mttr != 0:
            maintanability = 1.0/mttr
            
        fiability = 0
        if mtbf != 0:
            fiability = 1.0/mtbf
        
        
        report["incidents_length"] =  len(i_queryset)
        report["incidents_mttr"] =  mttr_hr
        report["incidents_mtbf"] =  mtbf_hr
        report["availability"] = availability
        report["maintanability"] = maintanability
        report["fiability"] = fiability
        
        l_inc_gravity = list()
        for gravity in self.list_incident_gravity():
            
            incident_by_gravity = {}
            incident_by_gravity["label"] = gravity
            incident_by_gravity["value"] = len(self.incidents_by_gravity(gravity))
            incident_by_gravity["color"] = colors_pool[cpt_color]
            l_inc_gravity.append(incident_by_gravity)
            cpt_color = cpt_color +1
            if cpt_color == 6:
                cpt_color = 0
                
        l_inc_type = list()
        for typ in self.list_incident_type():
            
            incident_by_type = {}
            incident_by_type["label"] = typ
            incident_by_type["value"] = len(self.incidents_by_type(typ))
            incident_by_type["color"] = colors_pool[cpt_color]
            l_inc_type.append(incident_by_type)
            cpt_color = cpt_color +1
            if cpt_color == 6:
                cpt_color = 0
                
        l_inc_state = list()
        for state in self.list_incident_state():
            
            incident_by_state = {}
            incident_by_state["label"] = state
            incident_by_state["value"] = len(self.incidents_by_state(state))
            incident_by_state["color"] = colors_pool[cpt_color]
            l_inc_state.append(incident_by_state)
            cpt_color = cpt_color +1
            if cpt_color == 6:
                cpt_color = 0
            
            
        report["incident_by_gravity"] = l_inc_gravity
        report["incident_by_type"] = l_inc_type
        report["incident_by_state"] = l_inc_state
        
        return report
    
    def get_problem_report_data(self):
        
        from src.business.evenement.evenement import Problem
        
        report = {}
        
        cpt_color = 0
        
        colors_pool = ["#bca349","#2081c1","#d0743c","#69a5f9","#98a9c5", "#e4a049"]
        
        i_queryset = Problem.objects
           
        mttr, mttr_hr = self.compute_problem_mttr()
       
        report["problems_length"] =  len(i_queryset)
        report["problems_mttr"] =  mttr_hr
        
        l_pb_priority = list()
        for priority in self.list_problem_priority():
            
            problem_by_priority = {}
            problem_by_priority["label"] = priority
            problem_by_priority["value"] = len(self.problems_by_priority(priority))
            problem_by_priority["color"] = colors_pool[cpt_color]
            l_pb_priority.append(problem_by_priority)
            cpt_color = cpt_color +1
            if cpt_color == 6:
                cpt_color = 0
                
        l_pb_type = list()
        for typ in self.list_problem_type():
            
            problem_by_type = {}
            problem_by_type["label"] = typ
            problem_by_type["value"] = len(self.problems_by_type(typ))
            problem_by_type["color"] = colors_pool[cpt_color]
            l_pb_type.append(problem_by_type)
            cpt_color = cpt_color +1
            if cpt_color == 6:
                cpt_color = 0
                
        l_pb_state = list()
        for state in self.list_problem_state():
            
            problem_by_state = {}
            problem_by_state["label"] = state
            problem_by_state["value"] = len(self.problems_by_state(state))
            problem_by_state["color"] = colors_pool[cpt_color]
            l_pb_state.append(problem_by_state)
            cpt_color = cpt_color +1
            if cpt_color == 6:
                cpt_color = 0
            
            
        report["problem_by_priority"] = l_pb_priority
        report["problem_by_type"] = l_pb_type
        report["problem_by_state"] = l_pb_state
        
        return report
    

    def compute_incident_mtbf(self):
        
        from src.business.evenement.evenement import Incident
        
        days = 0
        hour = 0
        minutes = 0
        sec = 0
        mtbf = 0
        total_ttf = 0
        n_repair = 0
        i_queryset = Incident.objects.order_by("+incident_date")
        if len(i_queryset) > 0:
            previous_item = i_queryset[0]
            for item in i_queryset[1:]:
                if  item.state == "resolved" and item.confirm:
                    ts = (item.incident_date - previous_item.incident_date).total_seconds()
                    ts = int(ts)
                    if ts < 0:
                        ts = ts * -1
                    total_ttf = total_ttf + ts
                    n_repair = n_repair + 1
                    previous_item = item
                    
            if n_repair == 0: #for avoid zero division
                n_repair = 1
            
            mtbf = int(total_ttf / n_repair)
            
            days = mtbf/86400
            hour = (mtbf%86400)/3600
            minutes = ((mtbf%86400)%3600)/60
            sec = ((mtbf%86400)%3600)%60
        
        return mtbf, str(days)+" jours, "+str(hour)+" heures, "+str(minutes)+" minutes, "+str(sec)+" secondes"
            
                
        
    def compute_incident_mttr(self):
        
        from src.business.evenement.evenement import Incident
        
        
        i_queryset = Incident.objects
        total_ttr = 0
        n_repair = 0
        
        for item in i_queryset:
            if  item.state == "resolved" and item.confirm:
                ts = (item.resolution_date - item.incident_date).total_seconds()
                total_ttr = total_ttr + ts
                n_repair = n_repair + 1
                
        if n_repair == 0: #for avoid zero division
            n_repair = 1
        
        mttr = int(total_ttr / n_repair)
        
        days = mttr/86400
        hour = (mttr%86400)/3600
        minutes = ((mttr%86400)%3600)/60
        sec = ((mttr%86400)%3600)%60
        return mttr, str(days)+" jours, "+str(hour)+" heures, "+str(minutes)+" minutes, "+str(sec)+" secondes"
    
    
    def compute_change_mtbc(self):
        
        from src.business.evenement.evenement import Change
        
        days = 0
        hour = 0
        minutes = 0
        sec = 0
        mtbc = 0
        total_ttc = 0
        n_change = 0
        i_queryset = Change.objects.order_by("+change_date")
        if len(i_queryset) > 0:
            previous_item = i_queryset[0]
            for item in i_queryset[1:]:
                ts = (item.change_date - previous_item.change_date).total_seconds()
                total_ttc = total_ttc + ts
                n_change = n_change + 1
                previous_item = item
                    
            if n_change == 0: #for avoid zero division
                n_change = 1
            
            mtbc = int(total_ttc / n_change)
            
            days = mtbc/86400
            hour = (mtbc%86400)/3600
            minutes = ((mtbc%86400)%3600)/60
            sec = ((mtbc%86400)%3600)%60
        return mtbc, str(days)+" jours, "+str(hour)+" heures, "+str(minutes)+" minutes, "+str(sec)+" secondes"
    
    def compute_problem_mttr(self):
        
        from src.business.evenement.evenement import Problem
        
        
        i_queryset = Problem.objects
        total_ttr = 0
        n_repair = 0
        
        for item in i_queryset:
            if  item.state == "resolved":
                ts = (item.resolution_date - item.problem_date).total_seconds()
                total_ttr = total_ttr + ts
                n_repair = n_repair + 1
                
        if n_repair == 0: #for avoid zero division
            n_repair = 1
        
        mttr = int(total_ttr / n_repair)
        
        days = mttr/86400
        hour = (mttr%86400)/3600
        minutes = ((mttr%86400)%3600)/60
        sec = ((mttr%86400)%3600)%60
        return mttr, str(days)+" jours, "+str(hour)+" heures, "+str(minutes)+" minutes, "+str(sec)+" secondes"
    
    def list_incident_gravity(self):
        
        from src.business.evenement.evenement import Incident
         
        l_gravity = Incident.objects.distinct("gravity")
        
        return l_gravity
    
    def list_incident_type(self):
        
        from src.business.evenement.evenement import Incident
         
        l_type = Incident.objects.distinct("incident_type")
        
        return l_type
    
    def list_incident_state(self):
        
        from src.business.evenement.evenement import Incident
         
        l_state = Incident.objects.distinct("state")
        
        return l_state
    
    def list_problem_priority(self):
        
        from src.business.evenement.evenement import Problem
         
        l_priority = Problem.objects.distinct("priority")
        
        return l_priority
    
    def list_problem_type(self):
        
        from src.business.evenement.evenement import Problem
         
        l_type = Problem.objects.distinct("problem_type")
        
        return l_type
    
    def list_problem_state(self):
        
        from src.business.evenement.evenement import Problem
         
        l_state = Problem.objects.distinct("state")
        
        return l_state
    
    def list_change_type(self):
        
        from src.business.evenement.evenement import Change
         
        l_change = Change.objects.distinct("change_type")
        
        return l_change
    
    def incidents_by_gravity(self, _gravity):
        from src.business.evenement.evenement import Incident
        l_inc = Incident.objects(gravity = _gravity)
        return l_inc
    
    def incidents_by_type(self, _type):
        from src.business.evenement.evenement import Incident
        l_inc = Incident.objects(incident_type = _type)
        return l_inc
    
    def incidents_by_state(self, _state):
        from src.business.evenement.evenement import Incident
        l_inc = Incident.objects(state = _state)
        return l_inc
    
    def problems_by_priority(self, _priority):
        from src.business.evenement.evenement import Problem
        l_pb = Problem.objects(priority = _priority)
        return l_pb
    
    def problems_by_type(self, _type):
        from src.business.evenement.evenement import Problem
        l_pb = Problem.objects(problem_type = _type)
        return l_pb
    
    def problems_by_state(self, _state):
        from src.business.evenement.evenement import Problem
        l_pb = Problem.objects(state = _state)
        return l_pb
    
    def changes_by_type(self, _type):
        from src.business.evenement.evenement import Change
        l_change = Change.objects(change_type = _type)
        return l_change
        