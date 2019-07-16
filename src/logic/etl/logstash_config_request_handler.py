# coding: utf-8 
'''
Created on 4 sept. 2016

@author: kengne
'''

from flask import Blueprint, request
from flask.views import MethodView
from src.technique.security.security import requires_session_auth, requires_permission

logstash_config_url_register = Blueprint('logstash_config_urls', __name__, template_folder='../../view/web_assets/templates/')


# request handler.
class NewLogstashConfigPoolView(MethodView):
    
    @requires_session_auth
    @requires_permission("IT_ADMIN")
    def get(self):
        from src.view.python_views.etl.logstash_config import LogstashConfigPoolDialogue
        return LogstashConfigPoolDialogue().create_config_pool()
    
    @requires_session_auth
    @requires_permission("IT_ADMIN")
    def post(self):
        
        from src.view.python_views.etl.logstash_config import EditLogstashConfigPoolDialogue
        
        
        etl_machine_address  = request.form['etl_machine_address']
        etl_machine_username = request.form['etl_machine_username']
        etl_machine_password = request.form['etl_machine_password']
        etl_machine_rsa_ssh_key = request.form['etl_machine_rsa_ssh_key']
        etl_pool_name = request.form['etl_pool_name']
        etl_lauch_command = request.form['etl_lauch_command']
        etl_config_path_dir = request.form['etl_config_path_dir']
        is_manual_launch = request.form['is_manual_launch']
        
        if is_manual_launch == "on":
            is_manual_launch = True
        else:
            is_manual_launch = False
        
        return EditLogstashConfigPoolDialogue().create_config_pool(etl_machine_address, etl_machine_username, etl_machine_password, etl_machine_rsa_ssh_key, etl_pool_name, etl_lauch_command, etl_config_path_dir, is_manual_launch)

    

class UpdateLogstashConfigPoolView(MethodView):

    @requires_session_auth
    @requires_permission("IT_ADMIN") 
    def get(self, id_config_pool):
        from src.view.python_views.etl.logstash_config import LogstashConfigPoolDialogue
        return LogstashConfigPoolDialogue().update_config_pool(id_config_pool)
    
    @requires_session_auth
    @requires_permission("IT_ADMIN") 
    def post(self, id_config_pool):
        from src.view.python_views.etl.logstash_config import EditLogstashConfigPoolDialogue
        
        
        etl_machine_address  = request.form['etl_machine_address']
        etl_machine_username = request.form['etl_machine_username']
        etl_machine_password = request.form['etl_machine_password']
        etl_machine_rsa_ssh_key = request.form['etl_machine_rsa_ssh_key']
        etl_pool_name = request.form['etl_pool_name']
        etl_lauch_command = request.form['etl_lauch_command']
        etl_config_path_dir = request.form['etl_config_path_dir']
        is_manual_launch = request.form['is_manual_launch']
        if is_manual_launch == "on":
            is_manual_launch = True
        else:
            is_manual_launch = False
        
        return EditLogstashConfigPoolDialogue().update_config_pool(id_config_pool, etl_machine_address, etl_machine_username, etl_machine_password, etl_machine_rsa_ssh_key, etl_pool_name, etl_lauch_command, etl_config_path_dir, is_manual_launch)


        
class DeleteLogstashConfigPoolView(MethodView):
    
    
    @requires_session_auth
    @requires_permission("IT_ADMIN") 
    def get(self, id_config_pool):
        from src.view.python_views.etl.logstash_config import LogstashConfigPoolDialogue
        return LogstashConfigPoolDialogue().delete_config_pool(id_config_pool)
    

class ViewLogstashConfigPoolView(MethodView):

    @requires_session_auth
    @requires_permission("IT_ADMIN")
    def get(self, id_config_pool):
        from src.view.python_views.etl.logstash_config import LogstashConfigPoolDialogue
        return LogstashConfigPoolDialogue().view_config_pool(id_config_pool)
        

class ListLogstashConfigPoolView(MethodView):

    @requires_session_auth
    @requires_permission("IT_ADMIN")
    def get(self):
        from src.view.python_views.system.system import GrumosDefaultDialogue
        return GrumosDefaultDialogue().logstash_config()

class StartLogstashConfigPoolView(MethodView):

    @requires_session_auth
    @requires_permission("IT_ADMIN")
    def get(self, id_config_pool):
        from src.view.python_views.etl.logstash_config import LogstashConfigPoolDialogue
        return LogstashConfigPoolDialogue().start_config_pool(id_config_pool)
    

#=============================================================================
# Configuration file views    


class NewLogstashConfigFileView(MethodView):
    
    @requires_session_auth
    @requires_permission("IT_ADMIN")
    def get(self,id_config_pool):
        from src.view.python_views.etl.logstash_config import LogstashConfigFileDialogue
        return LogstashConfigFileDialogue().create_config_file(id_config_pool)
    
    @requires_session_auth
    @requires_permission("IT_ADMIN")
    def post(self, id_config_pool):
        
        from src.view.python_views.etl.logstash_config import EditLogstashConfigFileDialogue
        
        
        draft_config  = request.form['draft_config']
        etl_config_file = request.form['etl_config_file']
    
        
        return EditLogstashConfigFileDialogue().create_config_file(id_config_pool, draft_config, etl_config_file)

    

class UpdateLogstashConfigFileView(MethodView):

    @requires_session_auth
    @requires_permission("IT_ADMIN") 
    def get(self, id_config_pool, id_config_file):
        from src.view.python_views.etl.logstash_config import LogstashConfigFileDialogue
        return LogstashConfigFileDialogue().update_config_file(id_config_pool, id_config_file)
    
    @requires_session_auth
    @requires_permission("IT_ADMIN") 
    def post(self, id_config_pool, id_config_file):
        from src.view.python_views.etl.logstash_config import EditLogstashConfigFileDialogue
        
        
        draft_config  = request.form['draft_config']
        etl_config_file = request.form['etl_config_file']
    
        
        return EditLogstashConfigFileDialogue().update_config_file(id_config_pool, id_config_file, draft_config, etl_config_file)

        
class DeleteLogstashConfigFileView(MethodView):
    
    
    @requires_session_auth
    @requires_permission("IT_ADMIN") 
    def get(self,id_config_pool, id_config_file):
        from src.view.python_views.etl.logstash_config import LogstashConfigFileDialogue
        return LogstashConfigFileDialogue().delete_config_file(id_config_pool, id_config_file)
    

class ViewLogstashConfigFileView(MethodView):

    @requires_session_auth
    @requires_permission("IT_ADMIN")
    def get(self, id_config_file):
        from src.view.python_views.etl.logstash_config import LogstashConfigFileDialogue
        return LogstashConfigFileDialogue().view_config_file(id_config_file)
        


class SendLogstashConfigFileView(MethodView):

    @requires_session_auth
    @requires_permission("IT_ADMIN")
    def get(self, id_config_pool, id_config_file):
        from src.view.python_views.etl.logstash_config import LogstashConfigFileDialogue
        return LogstashConfigFileDialogue().send_config_file(id_config_pool, id_config_file)

class RestoreLogstashConfigFileView(MethodView):

    @requires_session_auth
    @requires_permission("IT_ADMIN")
    def get(self, id_config_pool, id_config_file):
        from src.view.python_views.etl.logstash_config import LogstashConfigFileDialogue
        return LogstashConfigFileDialogue().restore_config_file(id_config_pool, id_config_file)
    
    
    
        
# Register the urls
logstash_config_url_register.add_url_rule('/console/etl/logstashs/', view_func=ListLogstashConfigPoolView.as_view('list_config_pool_handler'))
logstash_config_url_register.add_url_rule('/console/etl/logstashs/create/', view_func=NewLogstashConfigPoolView.as_view('new_config_pool_handler'))
logstash_config_url_register.add_url_rule('/console/etl/logstashs/update/<id_config_pool>/', view_func=UpdateLogstashConfigPoolView.as_view('update_config_pool_handler'))
logstash_config_url_register.add_url_rule('/console/etl/logstashs/delete/<id_config_pool>/', view_func=DeleteLogstashConfigPoolView.as_view('delete_config_pool_handler'))
logstash_config_url_register.add_url_rule('/console/etl/logstashs/view/<id_config_pool>/', view_func=ViewLogstashConfigPoolView.as_view('view_config_pool_handler'))
logstash_config_url_register.add_url_rule('/console/etl/logstashs/start_pool/<id_config_pool>/', view_func=StartLogstashConfigPoolView.as_view('start_config_pool_handler'))



logstash_config_url_register.add_url_rule('/console/etl/logstashs/configfile/create/<id_config_pool>/', view_func=NewLogstashConfigFileView.as_view('new_config_file_handler'))
logstash_config_url_register.add_url_rule('/console/etl/logstashs/configfile/update/<id_config_pool>/<id_config_file>/', view_func=UpdateLogstashConfigFileView.as_view('update_config_file_handler'))
logstash_config_url_register.add_url_rule('/console/etl/logstashs/configfile/delete/<id_config_pool>/<id_config_file>/', view_func=DeleteLogstashConfigFileView.as_view('delete_config_file_handler'))
logstash_config_url_register.add_url_rule('/console/etl/logstashs/configfile/view/<id_config_file>/', view_func=ViewLogstashConfigFileView.as_view('view_config_file_handler'))
logstash_config_url_register.add_url_rule('/console/etl/logstashs/configfile/send_to_logstash/<id_config_pool>/<id_config_file>/', view_func=SendLogstashConfigFileView.as_view('send_config_file_handler'))
logstash_config_url_register.add_url_rule('/console/etl/logstashs/configfile/restore/<id_config_pool>/<id_config_file>/', view_func=RestoreLogstashConfigFileView.as_view('restore_config_file_handler'))
