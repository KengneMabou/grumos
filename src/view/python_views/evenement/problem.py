# coding: utf-8 
'''
Created on 14 oct. 2016

@author: kengne
'''
from src.view.python_views.utils.dialogue import GenericDialogue
from flask import render_template, redirect, url_for

class EditProblemDialogue(GenericDialogue):
    
    name = ""
    description = ""
    machines_impacted = ""
    problem_type = ""
    services_impacted = ""
    priority = ""
    confirm = "" 
    problem_date = ""
    resolution_date = "" 
    state = ""
    
    
    def create_problem(self, name, description, machines_impacted, problem_type, services_impacted, priority, confirm, problem_date, resolution_date, state):
        
        from src.logic.evenement.problem_logic import ProblemLogic
        from src.logic.monitoring.monitoring_component_logic import MonitoringComponentLogic
        from src.logic.monitoring.services_component_logic import ServicesComponentLogic
        
        plog = ProblemLogic()
        
        list_problem_type = ['hardware', 'network', 'system', "software service", "docker container"]
        list_priority = ['low', 'medium', 'high']
        list_state = ['open', 'resolved', 'non resolved']
        
        mcl = MonitoringComponentLogic()
        scl = ServicesComponentLogic()
        
        list_machines = mcl.list_machines()
        list_services = scl.list_services()
        
        
        error = plog.create_problem(name, description, machines_impacted, problem_type, services_impacted, priority, confirm, problem_date, resolution_date, state)
        
        if not error:
            return ProblemDialogue().ouvrir_par_redirection()
        else:
            context_data = {"destination_url": url_for('problem_urls.new_problem_handler'),
                            "name": name,
                            "description": description,
                            "machines_impacted" : machines_impacted,
                            "problem_type" : problem_type,
                            "services_impacted" : services_impacted,
                            "priority" : priority, 
                            "confirm" : confirm, 
                            "problem_date" : problem_date, 
                            "resolution_date" : resolution_date, 
                            "state" : state,
                            "list_problem_type" : list_problem_type,
                            "list_machines" : list_machines,
                            "list_services" : list_services,
                            "list_priority" : list_priority,
                            "list_state" : list_state,
                            "update_mode":False,
                            "error":error,
                        }
            return self.ouvrir(context_data) 
        
        
        
        
    def update_problem(self, id_problem, name, description, machines_impacted, problem_type, services_impacted, priority, confirm, problem_date, resolution_date, state):
        
        from src.logic.evenement.problem_logic import ProblemLogic
        from src.logic.monitoring.monitoring_component_logic import MonitoringComponentLogic
        from src.logic.monitoring.services_component_logic import ServicesComponentLogic
        
        plog = ProblemLogic()
        
        list_problem_type = ['hardware', 'network', 'system', "software service", "docker container"]
        list_priority = ['low', 'medium', 'high']
        list_state = ['open', 'resolved', 'non resolved']
        mcl = MonitoringComponentLogic()
        scl = ServicesComponentLogic()
        
        list_machines = mcl.list_machines()
        list_services = scl.list_services()
        
        error = plog.update_problem(id_problem, name, description, machines_impacted, problem_type, services_impacted, priority, confirm, problem_date, resolution_date, state)
        if not error:
            return ProblemDialogue().ouvrir_par_redirection()
        else:
            context_data = {"destination_url": url_for('problem_urls.update_problem_handler', id_problem=id_problem),
                            "name": name,
                            "description": description,
                            "machines_impacted" : machines_impacted,
                            "problem_type" : problem_type,
                            "services_impacted" : services_impacted,
                            "priority" : priority, 
                            "confirm" : confirm, 
                            "problem_date" : problem_date, 
                            "resolution_date" : resolution_date, 
                            "state" : state,
                            "list_problem_type" : list_problem_type,
                            "list_machines" : list_machines,
                            "list_services" : list_services,
                            "list_priority" : list_priority,
                            "list_state" : list_state,
                            "update_mode":True,
                            "error":error,
                        }
            return self.ouvrir(context_data)
    
     
    def ouvrir(self, context_data=None):
        
        return render_template('grumos_templates/event/problem/form_problem.html', **context_data)
    
    def ouvrir_par_redirection(self, context_data=None):
        return redirect(url_for('problem_urls.new_problem_handler'))
    
    
class ProblemDialogue(GenericDialogue):
    
    list_problems = None
    
    def delete_problem(self, id_problem):
        from src.logic.evenement.problem_logic import ProblemLogic
        ProblemLogic().delete_problem(id_problem)
        return self.ouvrir_par_redirection()
            
    def update_problem(self, id_problem):
        
        from src.logic.evenement.problem_logic import ProblemLogic
        from src.logic.monitoring.monitoring_component_logic import MonitoringComponentLogic
        from src.logic.monitoring.services_component_logic import ServicesComponentLogic
        
        plog = ProblemLogic()
        
        list_problem_type = ['hardware', 'network', 'system', "software service", "docker container"]
        list_priority = ['low', 'medium', 'high']
        list_state = ['open', 'resolved', 'non resolved']
        mcl = MonitoringComponentLogic()
        scl = ServicesComponentLogic()
        
        list_machines = mcl.list_machines()
        list_services = scl.list_services()
        
        context_data = {}
        
        problem = plog.get_problem(id_problem)
        
        if problem : 
            
            context_data = {"destination_url": url_for('problem_urls.update_problem_handler', id_problem=problem.id),
                            "name": problem.name,
                            "description": problem.description,
                            "machines_impacted" : problem.machines_impacted,
                            "problem_type" : problem.problem_type,
                            "services_impacted" : problem.services_impacted,
                            "priority" : problem.priority, 
                            "confirm" : problem.confirm, 
                            "problem_date" : problem.problem_date, 
                            "resolution_date" : problem.resolution_date, 
                            "state" : problem.state,
                            "list_problem_type" : list_problem_type,
                            "list_machines" : list_machines,
                            "list_services" : list_services,
                            "list_priority" : list_priority,
                            "list_state" : list_state,
                            "update_mode":True,
                            "error":{},
                        }
        
        
        return EditProblemDialogue().ouvrir(context_data)
    
    def create_problem(self):
    
        from src.logic.monitoring.monitoring_component_logic import MonitoringComponentLogic
        from src.logic.monitoring.services_component_logic import ServicesComponentLogic
        
        list_problem_type = ['hardware', 'network', 'system', "software service", "docker container"]
        list_priority = ['low', 'medium', 'high']
        list_state = ['open', 'resolved', 'non resolved']
        mcl = MonitoringComponentLogic()
        scl = ServicesComponentLogic()
        
        list_machines = mcl.list_machines()
        list_services = scl.list_services()
        
        
        context_data = {"destination_url": url_for('problem_urls.new_problem_handler'),
                        "name": "",
                        "description": "",
                        "machines_impacted" : "",
                        "problem_type" : "",
                        "services_impacted" : "",
                        "priority" : "", 
                        "confirm" : "", 
                        "problem_date" : "", 
                        "resolution_date" : "", 
                        "state" :"",
                        "list_problem_type" : list_problem_type,
                        "list_machines" : list_machines,
                        "list_services" : list_services,
                        "list_priority" : list_priority,
                        "list_state" : list_state,
                        "update_mode":False,
                        "error":{},
                    }
        
        return EditProblemDialogue().ouvrir(context_data)
    
      
    def ouvrir (self, number_items, problem_type, page):
        
        from src.logic.evenement.problem_logic import ProblemLogic
        
        number_items = int(number_items)
        page = int(page) 
        data = ProblemLogic().filter_problems(number_items, problem_type, page)

        list_problem_type = {"all":"Tous","hardware":"hardware","network":"network", "system":"system", "software service":"software service", "docker container":"docker container"}
        list_number_items = [element * 10 for element in range(5)]
        next_page = page + 1
        previous_page = page - 1
        next_page = str(next_page)
        previous_page = str(previous_page)
        if problem_type is None:
            problem_type = "all"
        context = {
            "problems": data,
            "number_items":number_items,
            "problem_type":problem_type,
            "page":page,
            "next_page": next_page,
            "previous_page": previous_page,
            "list_problem_type":list_problem_type,
            "list_number_items":list_number_items,
            "filtering_url": url_for('problem_urls.list_problem_handler'),
            "new_problem_url": url_for('problem_urls.new_problem_handler'),
        }
        
        return render_template('grumos_templates/event/problem/list_problem.html', **context)        
            

    
    def ouvrir_par_redirection(self, context_data=None):
        return redirect(url_for('problem_urls.list_problem_handler', number_items = 30, problem_type = "all", page=1))
