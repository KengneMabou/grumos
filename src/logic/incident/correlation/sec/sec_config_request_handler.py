# coding: utf-8 
'''
Created on 4 sept. 2016
@author: kengne
'''

from flask import Blueprint, request
from flask.views import MethodView
from src.technique.security.security import requires_session_auth, requires_permission

sec_config_url_register = Blueprint('sec_config_urls', __name__, template_folder='../../view/web_assets/templates/')


# request handler.
class NewSecConfigPoolView(MethodView):
    
    @requires_session_auth
    @requires_permission("IT_ADMIN")
    def get(self):
        from src.view.python_views.incident.correlation.sec.sec_config import SecConfigPoolDialogue
        return SecConfigPoolDialogue().create_config_pool()
    
    @requires_session_auth
    @requires_permission("IT_ADMIN")
    def post(self):
        
        from src.view.python_views.incident.correlation.sec.sec_config import EditSecConfigPoolDialogue
        
        
        sec_machine_address  = request.form['sec_machine_address']
        sec_machine_username = request.form['sec_machine_username']
        sec_machine_password = request.form['sec_machine_password']
        sec_machine_rsa_ssh_key = request.form['sec_machine_rsa_ssh_key']
        sec_pool_name = request.form['sec_pool_name']
        sec_input_file = request.form['sec_input_file']
        sec_exec_file = request.form['sec_exec_file']
        sec_config_files_path = request.form['sec_config_files_path']
        
        
        return EditSecConfigPoolDialogue().create_config_pool(sec_machine_address, sec_machine_username, sec_machine_password, sec_machine_rsa_ssh_key, sec_pool_name, sec_input_file, sec_exec_file,sec_config_files_path)

    

class UpdateSecConfigPoolView(MethodView):

    @requires_session_auth
    @requires_permission("IT_ADMIN") 
    def get(self, id_config_pool):
        from src.view.python_views.incident.correlation.sec.sec_config import SecConfigPoolDialogue
        return SecConfigPoolDialogue().update_config_pool(id_config_pool)
    
    @requires_session_auth
    @requires_permission("IT_ADMIN") 
    def post(self, id_config_pool):
        from src.view.python_views.incident.correlation.sec.sec_config import EditSecConfigPoolDialogue
        
        
        sec_machine_address  = request.form['sec_machine_address']
        sec_machine_username = request.form['sec_machine_username']
        sec_machine_password = request.form['sec_machine_password']
        sec_machine_rsa_ssh_key = request.form['sec_machine_rsa_ssh_key']
        sec_pool_name = request.form['sec_pool_name']
        sec_input_file = request.form['sec_input_file']
        sec_exec_file = request.form['sec_exec_file']
        sec_config_files_path = request.form['sec_config_files_path']
        
        
        return EditSecConfigPoolDialogue().update_config_pool(id_config_pool, sec_machine_address, sec_machine_username, sec_machine_password, sec_machine_rsa_ssh_key, sec_pool_name, sec_input_file, sec_exec_file,sec_config_files_path)


        
class DeleteSecConfigPoolView(MethodView):
    
    
    @requires_session_auth
    @requires_permission("IT_ADMIN") 
    def get(self, id_config_pool):
        from src.view.python_views.incident.correlation.sec.sec_config import SecConfigPoolDialogue
        return SecConfigPoolDialogue().delete_config_pool(id_config_pool)
    

class ViewSecConfigPoolView(MethodView):

    @requires_session_auth
    @requires_permission("IT_ADMIN")
    def get(self, id_config_pool):
        from src.view.python_views.incident.correlation.sec.sec_config import SecConfigPoolDialogue
        return SecConfigPoolDialogue().view_config_pool(id_config_pool)
        

class ListSecConfigPoolView(MethodView):

    @requires_session_auth
    @requires_permission("IT_ADMIN")
    def get(self):
        from src.view.python_views.system.system import GrumosDefaultDialogue
        return GrumosDefaultDialogue().sec_config()

class StartSecConfigPoolView(MethodView):

    @requires_session_auth
    @requires_permission("IT_ADMIN")
    def get(self, id_config_pool):
        from src.view.python_views.incident.correlation.sec.sec_config import SecConfigPoolDialogue
        return SecConfigPoolDialogue().start_config_pool(id_config_pool)
    

#=============================================================================
# Configuration file views    


class NewSecConfigFileView(MethodView):
    
    @requires_session_auth
    @requires_permission("IT_ADMIN")
    def get(self,id_config_pool):
        from src.view.python_views.incident.correlation.sec.sec_config import SecConfigFileDialogue
        return SecConfigFileDialogue().create_config_file(id_config_pool)
    
    @requires_session_auth
    @requires_permission("IT_ADMIN")
    def post(self, id_config_pool):
        
        from src.view.python_views.incident.correlation.sec.sec_config import EditSecConfigFileDialogue
        
        
        draft_config  = request.form['draft_config']
        sec_config_file = request.form['sec_config_file']
    
        
        return EditSecConfigFileDialogue().create_config_file(id_config_pool, draft_config, sec_config_file)

    

class UpdateSecConfigFileView(MethodView):

    @requires_session_auth
    @requires_permission("IT_ADMIN") 
    def get(self, id_config_pool, id_config_file):
        from src.view.python_views.incident.correlation.sec.sec_config import SecConfigFileDialogue
        return SecConfigFileDialogue().update_config_file(id_config_pool, id_config_file)
    
    @requires_session_auth
    @requires_permission("IT_ADMIN") 
    def post(self, id_config_pool, id_config_file):
        from src.view.python_views.incident.correlation.sec.sec_config import EditSecConfigFileDialogue
        
        
        draft_config  = request.form['draft_config']
        sec_config_file = request.form['sec_config_file']
    
        
        return EditSecConfigFileDialogue().update_config_file(id_config_pool, id_config_file, draft_config, sec_config_file)

        
class DeleteSecConfigFileView(MethodView):
    
    
    @requires_session_auth
    @requires_permission("IT_ADMIN") 
    def get(self,id_config_pool, id_config_file):
        from src.view.python_views.incident.correlation.sec.sec_config import SecConfigFileDialogue
        return SecConfigFileDialogue().delete_config_file(id_config_pool, id_config_file)
    

class ViewSecConfigFileView(MethodView):

    @requires_session_auth
    @requires_permission("IT_ADMIN")
    def get(self, id_config_file):
        from src.view.python_views.incident.correlation.sec.sec_config import SecConfigFileDialogue
        return SecConfigFileDialogue().view_config_file(id_config_file)
        


class SendSecConfigFileView(MethodView):

    @requires_session_auth
    @requires_permission("IT_ADMIN")
    def get(self, id_config_pool, id_config_file):
        from src.view.python_views.incident.correlation.sec.sec_config import SecConfigFileDialogue
        return SecConfigFileDialogue().send_config_file(id_config_pool, id_config_file)

class RestoreSecConfigFileView(MethodView):

    @requires_session_auth
    @requires_permission("IT_ADMIN")
    def get(self, id_config_pool, id_config_file):
        from src.view.python_views.incident.correlation.sec.sec_config import SecConfigFileDialogue
        return SecConfigFileDialogue().restore_config_file(id_config_pool, id_config_file)
    
    
    
        
# Register the urls
sec_config_url_register.add_url_rule('/console/incident/correlation/sec/', view_func=ListSecConfigPoolView.as_view('list_config_pool_handler'))
sec_config_url_register.add_url_rule('/console/incident/correlation/sec/create/', view_func=NewSecConfigPoolView.as_view('new_config_pool_handler'))
sec_config_url_register.add_url_rule('/console/incident/correlation/sec/update/<id_config_pool>/', view_func=UpdateSecConfigPoolView.as_view('update_config_pool_handler'))
sec_config_url_register.add_url_rule('/console/incident/correlation/sec/delete/<id_config_pool>/', view_func=DeleteSecConfigPoolView.as_view('delete_config_pool_handler'))
sec_config_url_register.add_url_rule('/console/incident/correlation/sec/view/<id_config_pool>/', view_func=ViewSecConfigPoolView.as_view('view_config_pool_handler'))
sec_config_url_register.add_url_rule('/console/incident/correlation/sec/start_pool/<id_config_pool>/', view_func=StartSecConfigPoolView.as_view('start_config_pool_handler'))



sec_config_url_register.add_url_rule('/console/incident/correlation/sec/configfile/create/<id_config_pool>/', view_func=NewSecConfigFileView.as_view('new_config_file_handler'))
sec_config_url_register.add_url_rule('/console/incident/correlation/sec/configfile/update/<id_config_pool>/<id_config_file>/', view_func=UpdateSecConfigFileView.as_view('update_config_file_handler'))
sec_config_url_register.add_url_rule('/console/incident/correlation/sec/configfile/delete/<id_config_pool>/<id_config_file>/', view_func=DeleteSecConfigFileView.as_view('delete_config_file_handler'))
sec_config_url_register.add_url_rule('/console/incident/correlation/sec/configfile/view/<id_config_file>/', view_func=ViewSecConfigFileView.as_view('view_config_file_handler'))
sec_config_url_register.add_url_rule('/console/incident/correlation/sec/configfile/send_to_sec/<id_config_pool>/<id_config_file>/', view_func=SendSecConfigFileView.as_view('send_config_file_handler'))
sec_config_url_register.add_url_rule('/console/incident/correlation/sec/configfile/restore/<id_config_pool>/<id_config_file>/', view_func=RestoreSecConfigFileView.as_view('restore_config_file_handler'))
