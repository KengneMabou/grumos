'''
Created on 13 sept. 2016

@author: kengne
'''
from src.view.python_views.utils.dialogue import GenericDialogue
from flask import render_template, redirect, url_for

class LogstashConfigPoolDialogue(GenericDialogue):
    
    list_config_pool = None
    
    def delete_config_pool (self, id_config_pool):
        from src.logic.etl.logstash_config_logic import LogstashConfigPoolLogic
        LogstashConfigPoolLogic().delete_config_pool(id_config_pool)
        return self.ouvrir_par_redirection()
    
    def view_config_pool (self, id_config_pool):
        
        return LogstashConfigFileDialogue().ouvrir(id_config_pool)
        
    
    
    def update_config_pool (self, id_config_pool):
    
        from src.logic.etl.logstash_config_logic import LogstashConfigPoolLogic
        
        context_data = {}
        config_pool = LogstashConfigPoolLogic().get_config_pool(id_config_pool)
        
        if config_pool : 
            
            context_data = {"destination_url": url_for('logstash_config_urls.update_config_pool_handler', id_config_pool=config_pool.id),
                            "etl_machine_address":config_pool.etl_machine_address,
                            "etl_machine_username": config_pool.etl_machine_username,
                            "etl_machine_password": config_pool.etl_machine_password,
                            "etl_machine_rsa_ssh_key":config_pool.etl_machine_rsa_ssh_key,
                            "etl_pool_name": config_pool.etl_pool_name,
                            "etl_lauch_command":config_pool.etl_lauch_command, 
                            "etl_config_path_dir":config_pool.etl_config_path_dir,
                            "is_manual_launch":config_pool.is_manual_launch,
                            "update_mode":True,
                            "error":{},
                        }
        
        
        return EditLogstashConfigPoolDialogue().ouvrir(context_data)
    
    def start_config_pool (self, id_config_pool):
    
        from src.logic.etl.logstash_config_logic import LogstashConfigPoolLogic
        
        start_config_pool_msg = LogstashConfigPoolLogic().start_config_pool(id_config_pool)
        return self.ouvrir(start_config_pool_msg)
        
    def create_config_pool (self):
    
            
        context_data = {"destination_url": url_for('logstash_config_urls.new_config_pool_handler'),
                        "etl_machine_address":"",
                        "etl_machine_username": "",
                        "etl_machine_password": "",
                        "etl_machine_rsa_ssh_key":"",
                        "etl_pool_name": "",
                        "etl_lauch_command":"", 
                        "etl_config_path_dir":"",
                        "is_manual_launch":"",
                        "update_mode":False,
                        "error":{},
                    }
        
        
        return EditLogstashConfigPoolDialogue().ouvrir(context_data)
            
    
    
    def ouvrir (self, extra_data = None):
        from src.logic.etl.logstash_config_logic import LogstashConfigPoolLogic
        
        data = LogstashConfigPoolLogic().list_config_pools()
        
        context = {
            "config_pools": data,
            "launch_logstash_msg":extra_data,
            "new_config_pool_url": url_for('logstash_config_urls.new_config_pool_handler'),
        }
        
        return render_template('grumos_templates/etl/logstash_config/list_logstash_config_pool.html', **context)
              
            

    
    def ouvrir_par_redirection(self, context_data=None):
        return redirect(url_for('logstash_config_urls.list_config_pool_handler'))
    

class EditLogstashConfigPoolDialogue(GenericDialogue):
    
    

    etl_machine_address= "",
    etl_machine_username = "",
    etl_machine_password = "",
    etl_pool_name = "",
    etl_lauch_command = "", 
    etl_config_path_dir = "",
    is_manual_launch = "",
                        
    def create_config_pool(self, etl_machine_address, etl_machine_username, etl_machine_password, etl_machine_rsa_ssh_key, etl_pool_name, etl_lauch_command, etl_config_path_dir, is_manual_launch):
        
        from src.logic.etl.logstash_config_logic import LogstashConfigPoolLogic
        
        
        error = LogstashConfigPoolLogic().create_config_pool(etl_machine_address, etl_machine_username, etl_machine_password, etl_machine_rsa_ssh_key,  etl_pool_name, etl_lauch_command, etl_config_path_dir, is_manual_launch)
        
        if not error:
            return LogstashConfigPoolDialogue().ouvrir_par_redirection()
        else:
            context_data = {"destination_url": url_for('logstash_config_urls.new_config_pool_handler'),
                            "etl_machine_address":etl_machine_address,
                            "etl_machine_username": etl_machine_username,
                            "etl_machine_password": etl_machine_password,
                            "etl_machine_rsa_ssh_key":etl_machine_rsa_ssh_key,
                            "etl_pool_name": etl_pool_name,
                            "etl_lauch_command":etl_lauch_command, 
                            "etl_config_path_dir":etl_config_path_dir,
                            "is_manual_launch":is_manual_launch,
                            "update_mode":False,
                            "error":error,
                        }
            return self.ouvrir(context_data) 
        
        
        
        
    def update_config_pool(self, id_config_pool, etl_machine_address, etl_machine_username, etl_machine_password, etl_machine_rsa_ssh_key, etl_pool_name, etl_lauch_command, etl_config_path_dir, is_manual_launch):
        
        from src.logic.etl.logstash_config_logic import LogstashConfigPoolLogic
        
        
        error = LogstashConfigPoolLogic().update_config_pool(id_config_pool, etl_machine_address, etl_machine_username, etl_machine_password, etl_machine_rsa_ssh_key, etl_pool_name, etl_lauch_command, etl_config_path_dir, is_manual_launch)
        
        if not error:
            return LogstashConfigPoolDialogue().ouvrir_par_redirection()
        else:
            context_data = {"destination_url": url_for('logstash_config_urls.update_config_pool_handler', id_config_pool =id_config_pool),
                            "etl_machine_address":etl_machine_address,
                            "etl_machine_username": etl_machine_username,
                            "etl_machine_password": etl_machine_password,
                            "etl_machine_rsa_ssh_key":etl_machine_rsa_ssh_key,
                            "etl_pool_name": etl_pool_name,
                            "etl_lauch_command":etl_lauch_command, 
                            "etl_config_path_dir":etl_config_path_dir,
                            "is_manual_launch":is_manual_launch,
                            "update_mode":True,
                            "error":error,
                        }
            return self.ouvrir(context_data) 
    
     
    def ouvrir(self, context_data=None):
        
        return render_template('grumos_templates/etl/logstash_config/form_logstash_config_pool.html', **context_data)
    
    def ouvrir_par_redirection(self, context_data=None):
        return redirect(url_for('logstash_config_urls.new_config_pool_handler'))
    


#=======================================================================================
# Config file dialogue

class LogstashConfigFileDialogue(GenericDialogue):
    
    list_config_files = None
    
    def delete_config_file (self, id_config_pool, id_config_file):
        from src.logic.etl.logstash_config_logic import LogstashConfigFileLogic
        LogstashConfigFileLogic().delete_config_file(id_config_pool, id_config_file)
        return self.ouvrir_par_redirection(id_config_pool)
    
    def view_config_file(self, id_config_file):
        
        return ViewLogstashConfigFileDialogue().ouvrir(id_config_file)
        
    
    
    def update_config_file (self, id_config_pool, id_config_file):
    
        from src.logic.etl.logstash_config_logic import LogstashConfigFileLogic
        
        context_data = {}
        lcfl = LogstashConfigFileLogic()
        
        config_file=  lcfl.get_config_file(id_config_file)
        
        if config_file.draft_config == "" and config_file.previous_runing_config == "":
            config_file.draft_config = lcfl.get_remote_config_file(id_config_pool, id_config_file)
        if config_file : 
            
            context_data = {"destination_url": url_for('logstash_config_urls.update_config_file_handler', id_config_pool = id_config_pool , id_config_file=config_file.id),
                            "draft_config":config_file.draft_config,
                            "etl_config_file": config_file.etl_config_file,
                            "update_mode":True,
                            "error":{},
                        }
        
        
        return EditLogstashConfigFileDialogue().ouvrir(context_data)
    
        
    def create_config_file(self,id_config_pool):
    
            
        context_data = {"destination_url": url_for('logstash_config_urls.new_config_file_handler', id_config_pool = id_config_pool),
                        "draft_config": "",
                        "etl_config_file": "",
                        "update_mode":False,
                        "error":{},
                    }
        
        
        return EditLogstashConfigFileDialogue().ouvrir(context_data)
            
    def restore_config_file (self, id_config_pool, id_config_file):
    
        from src.logic.etl.logstash_config_logic import LogstashConfigFileLogic
        
        LogstashConfigFileLogic().restore_config_file(id_config_file)
        return LogstashConfigFileDialogue().ouvrir_par_redirection(id_config_pool)
    
    def send_config_file (self, id_config_pool, id_config_file):
    
        from src.logic.etl.logstash_config_logic import LogstashConfigFileLogic
        
        LogstashConfigFileLogic().send_config_file(id_config_pool, id_config_file)
        return LogstashConfigFileDialogue().ouvrir_par_redirection(id_config_pool)
    
    def ouvrir (self, id_config_pool, extra_data = None):
        from src.logic.etl.logstash_config_logic import LogstashConfigFileLogic
        from src.logic.etl.logstash_config_logic import LogstashConfigPoolLogic
        
        file_logic = LogstashConfigFileLogic()
        pool_logic = LogstashConfigPoolLogic()
        data = file_logic.get_config_files_onConfigPool(id_config_pool)
        
        context = {
            "config_files": data,
            "id_config_pool":id_config_pool,
            "config_pool_name": pool_logic.get_config_pool(id_config_pool).etl_pool_name,
            "new_config_file_url": url_for('logstash_config_urls.new_config_file_handler', id_config_pool = id_config_pool),
        }
        
        return render_template('grumos_templates/etl/logstash_config/list_logstash_config_file.html', **context)
              
            

    
    def ouvrir_par_redirection(self, id_config_pool, context_data=None):
        return redirect(url_for('logstash_config_urls.view_config_pool_handler', id_config_pool = id_config_pool) )
    
    
class EditLogstashConfigFileDialogue(GenericDialogue):
    
    

    draft_config = ""
    previous_runing_config = ""
    etl_config_file = ""
                        
    def create_config_file(self, id_config_pool, draft_config, etl_config_file):
        
        from src.logic.etl.logstash_config_logic import LogstashConfigFileLogic
        
        
        res = LogstashConfigFileLogic().create_config_file(id_config_pool, draft_config, etl_config_file)
        
        if not res['error']:
            return LogstashConfigFileDialogue().ouvrir_par_redirection(id_config_pool)
        else:
            context_data = {"destination_url": url_for('logstash_config_urls.new_config_file_handler', id_config_pool = id_config_pool),
                            "draft_config": draft_config,
                            "etl_config_file": etl_config_file,
                            "update_mode":False,
                            "error":res['error'],
                        }
            return self.ouvrir(context_data) 
        
        
        
        
    def update_config_file(self, id_config_pool, id_config_file, draft_config, etl_config_file):
        
        from src.logic.etl.logstash_config_logic import LogstashConfigFileLogic
        
        
        res = LogstashConfigFileLogic().update_config_file(id_config_file, draft_config, etl_config_file)
        
        if not res['error']:
            return LogstashConfigFileDialogue().ouvrir_par_redirection(id_config_pool)
        else:
            context_data = {"destination_url": url_for('logstash_config_urls.update_config_file_handler',id_config_pool = id_config_pool,id_config_file=id_config_file),
                            "draft_config": draft_config,
                            "etl_config_file": etl_config_file,
                            "update_mode":True,
                            "error":res['error'],
                        }
            return self.ouvrir(context_data) 
    
     
    def ouvrir(self, context_data=None):
        
        return render_template('grumos_templates/etl/logstash_config/form_logstash_config_file.html', **context_data)
    
    def ouvrir_par_redirection(self, context_data=None):
        
        return redirect(url_for('logstash_config_urls.new_config_file_handler'))
    
class ViewLogstashConfigFileDialogue(GenericDialogue):
    
    
    def ouvrir (self, id_config_file, extra_data = None):
        from src.logic.etl.logstash_config_logic import LogstashConfigFileLogic
        
        data = LogstashConfigFileLogic().get_config_file(id_config_file)
        
        context = {
            "config_file_data": data.draft_config.split("\n"),
        }
        
        return render_template('grumos_templates/etl/logstash_config/view_logstash_config_file.html', **context)
              
            

    
    def ouvrir_par_redirection(self, context_data=None):
        pass