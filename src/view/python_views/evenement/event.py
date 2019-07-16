# coding: utf-8 
'''
Created on 12 sept. 2016

@author: kengne
'''

from src.view.python_views.utils.dialogue import GenericDialogue
from flask import render_template, redirect, url_for


class EventDialogue(GenericDialogue):
    
    list_events = None
    
    def delete_event (self, id_event):
        from src.logic.evenement.metric_logic import EventLogic
        EventLogic().delete_event(id_event)
        return self.ouvrir_par_redirection()
    
    
    def filter_event (self, number_items = 0, event_type = None):
    
        return self.ouvrir(number_items, event_type, page = 1)
            
    
    
    def ouvrir (self, number_items, event_type, page):
        from src.logic.evenement.metric_logic import EventLogic
        number_items = int(number_items)
        page = int(page) 
        data = EventLogic().list_events(number_items, event_type, page)
        #data = EventLogic().naive_list_events()
        list_event_type = {"all":"Tous","software service":"Logiciel", "system":u"Système", "docker container":"Containeur Docker", "network":u"Réseau"}
        list_number_items = [element * 10 for element in range(5)]
        next_page = page + 1
        previous_page = page - 1
        next_page = str(next_page)
        previous_page = str(previous_page)
        if event_type is None:
            event_type = "all"
        context = {
            "events": data,
            "number_items":number_items,
            "event_type":event_type,
            "page":page,
            "next_page": next_page,
            "previous_page": previous_page,
            "list_event_type":list_event_type,
            "list_number_items":list_number_items,
            "filtering_url": url_for('metric_urls.filter_metric_handler'),
        }
        
        return render_template('grumos_templates/event/metric/list_metric.html', **context)        
            

    
    def ouvrir_par_redirection(self, context_data=None):
        return redirect(url_for('metric_urls.list_metric_handler', number_items = 30, event_type = "all", page=1))