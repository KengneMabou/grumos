'''
Created on 13 sept. 2016

@author: kengne
'''
from src.view.python_views.utils.dialogue import GenericDialogue
from flask import render_template, redirect, url_for

class SecConfigPoolDialogue(GenericDialogue):
    
    list_config_pool = None
    
    def delete_config_pool (self, id_config_pool):
        from src.logic.incident.correlation.sec.sec_config_logic import SecConfigPoolLogic
        SecConfigPoolLogic().delete_config_pool(id_config_pool)
        return self.ouvrir_par_redirection()
    
    def view_config_pool (self, id_config_pool):
        
        return SecConfigFileDialogue().ouvrir(id_config_pool)
        
    
    
    def update_config_pool (self, id_config_pool):
    
        from src.logic.incident.correlation.sec.sec_config_logic import SecConfigPoolLogic
        
        context_data = {}
        config_pool = SecConfigPoolLogic().get_config_pool(id_config_pool)
        
        if config_pool : 
            
            context_data = {"destination_url": url_for('sec_config_urls.update_config_pool_handler', id_config_pool=config_pool.id),
                            "sec_machine_address":config_pool.sec_machine_address,
                            "sec_machine_username": config_pool.sec_machine_username,
                            "sec_machine_password": config_pool.sec_machine_password,
                            "sec_machine_rsa_ssh_key":config_pool.sec_machine_rsa_ssh_key,
                            "sec_pool_name": config_pool.sec_pool_name,
                            "sec_input_file":config_pool.sec_input_file, 
                            "sec_exec_file":config_pool.sec_exec_file,
                            "sec_config_files_path":config_pool.sec_config_files_path,
                            "update_mode":True,
                            "error":{},
                        }
        
        
        return EditSecConfigPoolDialogue().ouvrir(context_data)
    
    def start_config_pool (self, id_config_pool):
    
        from src.logic.incident.correlation.sec.sec_config_logic import SecConfigPoolLogic
        
        start_config_pool_msg = SecConfigPoolLogic().start_config_pool(id_config_pool)
        return self.ouvrir(start_config_pool_msg)
        
    def create_config_pool (self):
    
            
        context_data = {"destination_url": url_for('sec_config_urls.new_config_pool_handler'),
                        "sec_machine_address":"",
                        "sec_machine_username": "",
                        "sec_machine_password": "",
                        "sec_machine_rsa_ssh_key":"",
                        "sec_pool_name": "",
                        "sec_input_file":"", 
                        "sec_exec_file":"",
                        "sec_config_files_path":"",
                        "update_mode":False,
                        "error":{},
                    }
        
        
        return EditSecConfigPoolDialogue().ouvrir(context_data)
            
    
    
    def ouvrir (self, extra_data = None):
        from src.logic.incident.correlation.sec.sec_config_logic import SecConfigPoolLogic
        
        data = SecConfigPoolLogic().list_config_pools()
        
        context = {
            "config_pools": data,
            "launch_sec_msg":extra_data,
            "new_config_pool_url": url_for('sec_config_urls.new_config_pool_handler'),
        }
        
        return render_template('grumos_templates/incident/correlation/sec_config/list_sec_config_pool.html', **context)
              
            

    
    def ouvrir_par_redirection(self, context_data=None):
        return redirect(url_for('sec_config_urls.list_config_pool_handler'))
    

class EditSecConfigPoolDialogue(GenericDialogue):
    
    

    sec_machine_address= "",
    sec_machine_username = "",
    sec_machine_password = "",
    sec_machine_rsa_ssh_key = "",
    sec_pool_name = "",
    sec_input_file = "", 
    sec_exec_file = "",
    sec_config_files_path = "",
    
    def create_config_pool(self, sec_machine_address, sec_machine_username, sec_machine_password, sec_machine_rsa_ssh_key, sec_pool_name, sec_input_file, sec_exec_file,sec_config_files_path):
        
        from src.logic.incident.correlation.sec.sec_config_logic import SecConfigPoolLogic
        
        
        error = SecConfigPoolLogic().create_config_pool(sec_machine_address, sec_machine_username, sec_machine_password, sec_machine_rsa_ssh_key,  sec_pool_name, sec_input_file, sec_exec_file,sec_config_files_path)
        
        if not error:
            return SecConfigPoolDialogue().ouvrir_par_redirection()
        else:
            context_data = {"destination_url": url_for('sec_config_urls.new_config_pool_handler'),
                            "sec_machine_address":sec_machine_address,
                            "sec_machine_username": sec_machine_username,
                            "sec_machine_password": sec_machine_password,
                            "sec_machine_rsa_ssh_key":sec_machine_rsa_ssh_key,
                            "sec_pool_name": sec_pool_name,
                            "sec_input_file":sec_input_file, 
                            "sec_exec_file":sec_exec_file,
                            "sec_config_files_path":sec_config_files_path,
                            "update_mode":False,
                            "error":error,
                        }
            return self.ouvrir(context_data) 
        
        
        
        
    def update_config_pool(self, id_config_pool, sec_machine_address, sec_machine_username, sec_machine_password, sec_machine_rsa_ssh_key, sec_pool_name, sec_input_file, sec_exec_file,sec_config_files_path):
        
        from src.logic.incident.correlation.sec.sec_config_logic import SecConfigPoolLogic
        
        
        error = SecConfigPoolLogic().update_config_pool(id_config_pool, sec_machine_address, sec_machine_username, sec_machine_password, sec_machine_rsa_ssh_key, sec_pool_name, sec_input_file, sec_exec_file,sec_config_files_path)
        
        if not error:
            return SecConfigPoolDialogue().ouvrir_par_redirection()
        else:
            context_data = {"destination_url": url_for('sec_config_urls.update_config_pool_handler', id_config_pool =id_config_pool),
                            "sec_machine_address":sec_machine_address,
                            "sec_machine_username": sec_machine_username,
                            "sec_machine_password": sec_machine_password,
                            "sec_machine_rsa_ssh_key":sec_machine_rsa_ssh_key,
                            "sec_pool_name": sec_pool_name,
                            "sec_input_file":sec_input_file, 
                            "sec_exec_file":sec_exec_file,
                            "sec_config_files_path":sec_config_files_path,
                            "update_mode":True,
                            "error":error,
                        }
            return self.ouvrir(context_data) 
    
     
    def ouvrir(self, context_data=None):
        
        return render_template('grumos_templates/incident/correlation/sec_config/form_sec_config_pool.html', **context_data)
    
    def ouvrir_par_redirection(self, context_data=None):
        return redirect(url_for('sec_config_urls.new_config_pool_handler'))
    


#=======================================================================================
# Config file dialogue

class SecConfigFileDialogue(GenericDialogue):
    
    list_config_files = None
    
    def delete_config_file (self, id_config_pool, id_config_file):
        from src.logic.incident.correlation.sec.sec_config_logic import SecConfigFileLogic
        SecConfigFileLogic().delete_config_file(id_config_pool, id_config_file)
        return self.ouvrir_par_redirection(id_config_pool)
    
    def view_config_file(self, id_config_file):
        
        return ViewSecConfigFileDialogue().ouvrir(id_config_file)
        
    
    
    def update_config_file (self, id_config_pool, id_config_file):
    
        from src.logic.incident.correlation.sec.sec_config_logic import SecConfigFileLogic
        
        context_data = {}
        lcfl = SecConfigFileLogic()
        
        config_file=  lcfl.get_config_file(id_config_file)
        
        if config_file.draft_config == "" and config_file.previous_runing_config == "":
            config_file.draft_config = lcfl.get_remote_config_file(id_config_pool, id_config_file)
        if config_file : 
            
            context_data = {"destination_url": url_for('sec_config_urls.update_config_file_handler', id_config_pool = id_config_pool , id_config_file=config_file.id),
                            "draft_config":config_file.draft_config,
                            "sec_config_file": config_file.sec_config_file,
                            "update_mode":True,
                            "error":{},
                        }
        
        
        return EditSecConfigFileDialogue().ouvrir(context_data)
    
        
    def create_config_file(self,id_config_pool):
    
            
        context_data = {"destination_url": url_for('sec_config_urls.new_config_file_handler', id_config_pool = id_config_pool),
                        "draft_config": "",
                        "sec_config_file": "",
                        "update_mode":False,
                        "error":{},
                    }
        
        
        return EditSecConfigFileDialogue().ouvrir(context_data)
            
    def restore_config_file (self, id_config_pool, id_config_file):
    
        from src.logic.incident.correlation.sec.sec_config_logic import SecConfigFileLogic
        
        SecConfigFileLogic().restore_config_file(id_config_file)
        return SecConfigFileDialogue().ouvrir_par_redirection(id_config_pool)
    
    def send_config_file (self, id_config_pool, id_config_file):
    
        from src.logic.incident.correlation.sec.sec_config_logic import SecConfigFileLogic
        
        SecConfigFileLogic().send_config_file(id_config_pool, id_config_file)
        return SecConfigFileDialogue().ouvrir_par_redirection(id_config_pool)
    
    def ouvrir (self, id_config_pool, extra_data = None):
        from src.logic.incident.correlation.sec.sec_config_logic import SecConfigFileLogic
        from src.logic.incident.correlation.sec.sec_config_logic import SecConfigPoolLogic
        
        file_logic = SecConfigFileLogic()
        pool_logic = SecConfigPoolLogic()
        data = file_logic.get_config_files_onConfigPool(id_config_pool)
        
        context = {
            "config_files": data,
            "id_config_pool":id_config_pool,
            "config_pool_name": pool_logic.get_config_pool(id_config_pool).sec_pool_name,
            "new_config_file_url": url_for('sec_config_urls.new_config_file_handler', id_config_pool = id_config_pool),
        }
        
        return render_template('grumos_templates/incident/correlation/sec_config/list_sec_config_file.html', **context)
              
            

    
    def ouvrir_par_redirection(self, id_config_pool, context_data=None):
        return redirect(url_for('sec_config_urls.view_config_pool_handler', id_config_pool = id_config_pool) )
    
    
class EditSecConfigFileDialogue(GenericDialogue):
    
    

    draft_config = ""
    previous_runing_config = ""
    sec_config_file = ""
                        
    def create_config_file(self, id_config_pool, draft_config, sec_config_file):
        
        from src.logic.incident.correlation.sec.sec_config_logic import SecConfigFileLogic
        
        
        res = SecConfigFileLogic().create_config_file(id_config_pool, draft_config, sec_config_file)
        
        if not res['error']:
            return SecConfigFileDialogue().ouvrir_par_redirection(id_config_pool)
        else:
            context_data = {"destination_url": url_for('sec_config_urls.new_config_file_handler', id_config_pool = id_config_pool),
                            "draft_config": draft_config,
                            "sec_config_file": sec_config_file,
                            "update_mode":False,
                            "error":res['error'],
                        }
            return self.ouvrir(context_data) 
        
        
        
        
    def update_config_file(self, id_config_pool, id_config_file, draft_config, sec_config_file):
        
        from src.logic.incident.correlation.sec.sec_config_logic import SecConfigFileLogic
        
        
        res = SecConfigFileLogic().update_config_file(id_config_file, draft_config, sec_config_file)
        
        if not res['error']:
            return SecConfigFileDialogue().ouvrir_par_redirection(id_config_pool)
        else:
            context_data = {"destination_url": url_for('sec_config_urls.update_config_file_handler',id_config_pool = id_config_pool,id_config_file=id_config_file),
                            "draft_config": draft_config,
                            "sec_config_file": sec_config_file,
                            "update_mode":True,
                            "error":res['error'],
                        }
            return self.ouvrir(context_data) 
    
     
    def ouvrir(self, context_data=None):
        
        return render_template('grumos_templates/incident/correlation/sec_config/form_sec_config_file.html', **context_data)
    
    def ouvrir_par_redirection(self, context_data=None):
        
        return redirect(url_for('sec_config_urls.new_config_file_handler'))
    
class ViewSecConfigFileDialogue(GenericDialogue):
    
    
    def ouvrir (self, id_config_file, extra_data = None):
        from src.logic.incident.correlation.sec.sec_config_logic import SecConfigFileLogic
        
        data = SecConfigFileLogic().get_config_file(id_config_file)
        
        context = {
            "config_file_data": data.draft_config.split("\n"),
        }
        
        return render_template('grumos_templates/incident/correlation/sec_config/view_sec_config_file.html', **context)
              
            

    
    def ouvrir_par_redirection(self, context_data=None):
        pass