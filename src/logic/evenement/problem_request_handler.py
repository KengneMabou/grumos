# coding: utf-8 
'''
Created on 12 sept. 2016

@author: kengne
'''

from flask import Blueprint, request
from flask.views import MethodView
from src.technique.security.security import requires_session_auth, requires_permission

problem_url_register = Blueprint('problem_urls', __name__, template_folder='../../view/web_assets/templates/')


class NewProblemView(MethodView):
    
    @requires_session_auth
    @requires_permission("IT_ADMIN")
    def get(self):
        from src.view.python_views.evenement.problem import ProblemDialogue
        return ProblemDialogue().create_problem()
    
    @requires_session_auth
    @requires_permission("IT_ADMIN")
    def post(self):
        
        from src.view.python_views.evenement.problem import EditProblemDialogue
        
        name = request.form['name']
        description = request.form['description']
        machines_impacted = request.form.getlist('machines_impacted')
        problem_type = request.form['problem_type']
        services_impacted = request.form.getlist('services_impacted')
        priority = request.form['priority']
        confirm = request.form['confirm']
        problem_date = request.form['problem_date']
        resolution_date = request.form['resolution_date']
        state = request.form['state']
        
        if confirm == "on":
            confirm = True
        else:
            confirm = False
         
        return EditProblemDialogue().create_problem(name, description, machines_impacted, problem_type, services_impacted, priority, confirm, problem_date, resolution_date, state)

    

class UpdateProblemView(MethodView):

    @requires_session_auth
    @requires_permission("IT_ADMIN") 
    def get(self, id_problem):
        from src.view.python_views.evenement.problem import ProblemDialogue
        return ProblemDialogue().update_problem(id_problem)
    
    @requires_session_auth
    @requires_permission("IT_ADMIN") 
    def post(self, id_problem):
        from src.view.python_views.evenement.problem import EditProblemDialogue

        name = request.form['name']
        description = request.form['description']
        machines_impacted = request.form.getlist('machines_impacted')
        problem_type = request.form['problem_type']
        services_impacted = request.form.getlist('services_impacted')
        priority = request.form['priority']
        confirm = request.form['confirm']
        problem_date = request.form['problem_date']
        resolution_date = request.form['resolution_date']
        state = request.form['state']
        
        if confirm == "on":
            confirm = True
        else:
            confirm = False
        
        return EditProblemDialogue().update_problem(id_problem, name, description, machines_impacted, problem_type, services_impacted, priority, confirm, problem_date, resolution_date, state)
       
class DeleteProblemView(MethodView):
    
    
    @requires_session_auth
    @requires_permission("IT_ADMIN") 
    def get(self, id_problem):
        from src.view.python_views.evenement.problem import ProblemDialogue
        return ProblemDialogue().delete_problem(id_problem)
    

class ListProblemView(MethodView):

    @requires_session_auth
    @requires_permission("IT_ADMIN")
    def get(self):
        from src.view.python_views.system.system import GrumosDefaultDialogue
        problem_type = request.args.get('problem_type')
        number_items = request.args.get('number_items')
        page = request.args.get('page')
        
        if problem_type == "all":
            problem_type = None
        return GrumosDefaultDialogue().problems(number_items, problem_type, page)
    
    def post(self):
        from src.view.python_views.system.system import GrumosDefaultDialogue

        number_items = request.form['number_items']
        problem_type = request.form['problem_type']
        
        if problem_type == "all":
            problem_type = None
        
        return GrumosDefaultDialogue().problems(number_items, problem_type, 1)
    
        
# Register the urls
problem_url_register.add_url_rule('/console/events/problems/create', view_func=NewProblemView.as_view('new_problem_handler'))
problem_url_register.add_url_rule('/console/events/problems/update/<id_problem>/', view_func=UpdateProblemView.as_view('update_problem_handler'))
problem_url_register.add_url_rule('/console/events/problems/', view_func=ListProblemView.as_view('list_problem_handler'))
problem_url_register.add_url_rule('/console/events/problems/delete/<id_problem>/', view_func=DeleteProblemView.as_view('delete_problem_handler'))
