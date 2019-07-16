# coding: utf-8 
'''
Created on 12 sept. 2016

@author: kengne
'''

class ProblemLogic:
    
    
    problem = None

    
    def filter_problems(self, number_items = 0, problem_type = None, page = 1):
        
        from src.business.evenement.evenement import Problem
        
        problems = {}
        
        number_items = int(number_items)
        page = int(page) 
        
        if problem_type is None:
            problems = Problem.objects
        else:
            problems = Problem.objects(problem_type=problem_type)
            
        if number_items > 0:
            maxi = page*number_items
            mini = page*number_items - number_items
            problems = problems[mini:maxi]
            
            
        return problems

    def delete_problem(self, id_problem):
        from src.business.evenement.evenement import Problem
        
        error = None
        problem = Problem.objects(id=id_problem).first()
        
        if problem :
            problem.delete()
        
        return error
    

    def get_problem(self, id_problem):
        from src.business.evenement.evenement import Problem
        
        ch = Problem.objects(id=id_problem).first()
        
        return ch
          
    def list_problems(self):
        from src.business.evenement.evenement import Problem
        
        problems = Problem.objects.all()
        
        return problems


    def update_problem(self, id_problem, name, description, machines_impacted, problem_type, services_impacted, priority, confirm, problem_date, resolution_date, state):
        """
            Method for updating infos about a problem
        """
        from src.business.evenement.evenement import Problem
            
        error = self.validate_form_update(id_problem, name, description, machines_impacted, problem_type, services_impacted, priority, confirm, problem_date, resolution_date, state)
        if resolution_date == "":
            resolution_date = None
        if not error:
            problem =  Problem.objects(id=id_problem).first()
            problem.name = name
            problem.description = description
            problem.machines_impacted =machines_impacted
            problem.problem_type = problem_type
            problem.services_impacted = services_impacted
            problem.priority = priority
            problem.confirm = confirm
            problem.problem_date = problem_date
            problem.resolution_date = resolution_date
            problem.state = state            
            problem.save()
            
        return error
    
    def create_problem(self,name, description, machines_impacted, problem_type, services_impacted, priority, confirm, problem_date, resolution_date, state):
        """This method is for registring a new problem"""
        from src.business.evenement.evenement import Problem
        from flask import session
        from src.technique.application_init.settings_vars import session_attrs
        
        if resolution_date == "":
            resolution_date = None
        error = self.validate_form_create(name, description, machines_impacted, problem_type, services_impacted, priority, confirm, problem_date, resolution_date, state)
        if not error:
            Problem(name = name, description = description, machines_impacted = machines_impacted, problem_type = problem_type, services_impacted = services_impacted, priority = priority, confirm = confirm, problem_date = problem_date, resolution_date = resolution_date, state = state, problem_recorder = session[session_attrs.get('username_attr')]).save()
        
        return error
        
    def validate_form_create(self, name, description, machines_impacted, problem_type, services_impacted, priority, confirm, problem_date, resolution_date, state):
        
        """
        method for validating input data during problem creation process
        """
        
        error = None
          
        if name == "":
            if not error: 
                error = {}
            error["name_empty_error"] = u"Le nom du problème est obligatoire"
               
            
        if problem_date == "": #TODO , we are also going to put a regex-based control to see if the date has the correct format
            if not error: 
                error = {}
            error["problem_date_empty _error"] = u"la date du problème est obligatoire"
            
            
            
        return error
    
    def validate_form_update(self, id_problem,name, description, machines_impacted, problem_type, services_impacted, priority, confirm, problem_date, resolution_date, state):
        
        """
        method for validating input data during problem udpate process
        """
        
        error = None
        
            
        if name == "":
            if not error: 
                error = {}
            error["name_empty_error"] = u"Le nom du problème est obligatoire"
               
            
        if problem_date == "": #TODO , we are also going to put a regex-based control to see if the date has the correct format
            if not error: 
                error = {}
            error["problem_date_empty _error"] = u"la date du problème est obligatoire"
            
            
        return error
    
