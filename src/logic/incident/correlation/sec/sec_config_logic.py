# coding: utf-8
'''
Created on 13 sept. 2016

@author: kengne
'''
class SecConfigPoolLogic:
    
    
    config_pool = None
    
    
    def start_config_pool(self, id_config_pool):
        
        import paramiko, base64, time
        
        msg = list()
        
        
        #base64_server_rsa_ssh_key = "AAAAB3NzaC1yc2EAAAADAQABAAABAQDI4s0Fffscy3ZlHZt5KK3ME4hf2VpOmWFEyHiIHnaTQ2W2NTGvYGFFL2VQCDUKfPB6re4uP8/V0PdyLwc2oRDhwSXDH7fzcW3ACHZpQGN9gT/W3fDPfX1K3NDXDN5tswpKu8qETSf+anltCaoLYpxb8j2B0tZNbYa4ETqZ0e75qZ207RB6UgF5nDpSt5CEZUG3JY4X+QQTgM5CIivyw1PtdrtHCX2jnXdDPh3CKZEY8fXrqBBO2RoVpZYmWeDb4934ADPdc73OUcqQ3Qw4Qwb6HiUdFlYDVjS3nj3VXJvEVBjsC3gbKd77dp7hx3ZzOmBtFEkO0hirgkKF4xNP+//v"
        config_pool = self.get_config_pool(id_config_pool)
        key = paramiko.RSAKey(data=base64.decodestring(config_pool.sec_machine_rsa_ssh_key))
        client = paramiko.SSHClient()
        client.get_host_keys().add(config_pool.sec_machine_address, 'ssh-rsa', key)
        client.connect(config_pool.sec_machine_address, username=config_pool.sec_machine_username, password=config_pool.sec_machine_password)
        
        if config_pool.sec_config_files_path[-1] != "/":
            config_pool.sec_config_files_path+"/"
            config_pool.save()
        
        pid_file = 'pid'+time.time()+".pid"
        log_file = 'log'+time.time()+".log"
        client.exec_command(config_pool.sec_exec_file+" --detach --conf="+ config_pool.sec_config_files_path+"* --input="+config_pool.sec_input_file+" --fromstart --pid="+pid_file+" --log="+log_file)
        
        client.close()
        
        return msg
        

    def delete_config_pool(self, id_config_pool):
        from src.business.incident.correlation.sec.sec import SecConfigPool
        
        error = None
        config_pool = SecConfigPool.objects(id=id_config_pool).first()
        
        if config_pool :
            config_pool.delete()
        
        return error
    

    def get_config_pool(self, id_config_pool):
        from src.business.incident.correlation.sec.sec import SecConfigPool
        
        config_pool = SecConfigPool.objects(id=id_config_pool).first()
        
        return config_pool
          
    def list_config_pools(self):
        from src.business.incident.correlation.sec.sec import SecConfigPool
        
        config_pools = SecConfigPool.objects.all()
        
        return config_pools


    def update_config_pool(self, id_config_pool, sec_machine_address, sec_machine_username, sec_machine_password, sec_machine_rsa_ssh_key, sec_pool_name, sec_input_file, sec_exec_file,sec_config_files_path):
        """
            Method for updating infos about a sec config pool
        """
        from src.business.incident.correlation.sec.sec import SecConfigPool
        
       
        error = self.validate_form_update(id_config_pool, sec_machine_address, sec_machine_username, sec_machine_password, sec_machine_rsa_ssh_key, sec_pool_name, sec_input_file, sec_exec_file,sec_config_files_path)
        
        if not error:
            config_pool =  SecConfigPool.objects(id=id_config_pool).first()
            config_pool.sec_machine_address = sec_machine_address
            config_pool.sec_machine_username = sec_machine_username
            config_pool.sec_machine_password = sec_machine_password
            config_pool.sec_machine_rsa_ssh_key = sec_machine_rsa_ssh_key
            config_pool.sec_pool_name = sec_pool_name
            config_pool.sec_input_file = sec_input_file
            config_pool.sec_exec_file = sec_exec_file
            config_pool.sec_config_files_path = sec_config_files_path
            config_pool.save()
        return error
    
    def create_config_pool(self, sec_machine_address, sec_machine_username, sec_machine_password, sec_machine_rsa_ssh_key, sec_pool_name, sec_input_file, sec_exec_file, sec_config_files_path):
        """This method is for registring a new sec pool"""
        from src.business.incident.correlation.sec.sec import SecConfigPool
        error = self.validate_form_create(sec_machine_address, sec_machine_username, sec_machine_password, sec_machine_rsa_ssh_key, sec_pool_name, sec_input_file, sec_exec_file,sec_config_files_path)
        if not error:
            SecConfigPool(sec_machine_address = sec_machine_address , sec_machine_username = sec_machine_username, sec_machine_password = sec_machine_password, sec_machine_rsa_ssh_key = sec_machine_rsa_ssh_key, sec_pool_name = sec_pool_name, sec_input_file = sec_input_file, sec_exec_file = sec_exec_file, sec_config_files_path = sec_config_files_path).save()
        return error
        
        
    def validate_form_create(self, sec_machine_address, sec_machine_username, sec_machine_password, sec_machine_rsa_ssh_key, sec_pool_name, sec_input_file, sec_exec_file, sec_config_files_path):
        
        """
        method for validating input data during sec config pool creation process
        """
        from src.business.incident.correlation.sec.sec import SecConfigPool
        
        error = None
        
            
        config_pool = SecConfigPool.objects(sec_pool_name=sec_pool_name).first()
        
        if config_pool:
            if not error: 
                error = {}
            error["sec_pool_name_exist_error"] = u"Ce nom de pool existe déjà"
            
        if sec_machine_address == "":
            if not error: 
                error = {}
            error["sec_machine_address_empty_error"] = u"Vous devez spécifier une adresse IP valide"
                           
        if sec_machine_username == "":
            if not error: 
                error = {}
            error["sec_machine_username_empty_error"] = u"Vous devez spécifier un nom d'utilisateur valide pour une connexion ssh sur la machine Logstash"
            
        if sec_machine_password == "":
            if not error: 
                error = {}
            error["sec_machine_password_empty_error"] = u"Vous devez spécifier un mot de passe valide pour une connexion ssh sur la machine Logstash"
            
        if sec_pool_name == "":
            if not error: 
                error = {}
            error["sec_pool_name_empty_error"] = u"Vous devez spécifier un nom de pool et il doit être unique"
        
        if sec_input_file == "":
            if not error: 
                error = {}
            error["sec_input_file_empty_error"] = u"Vous devez spécifier le chemin absolu vers le fichier de données pour la corrélation"
        
        if sec_config_files_path == "":
            if not error: 
                error = {}
            error["sec_config_files_path_empty_error"] = u"Vous devez spécifier le chemin absolu du repertoire de ce pool de configuration Sec"

            
        if sec_exec_file == "":
            if not error: 
                error = {}
            error["sec_exec_file_empty_error"] = u"Vous devez spécifier le chemin absolu vers le fichier executable sec"
            
        if sec_machine_rsa_ssh_key == "":
            if not error: 
                error = {}
            error["sec_machine_rsa_ssh_key_empty_error"] = u"Vous devez spécifier la clé public RSA du serveur SSH de la machine sec"

            
            
        return error
    
    def validate_form_update(self, id_config_pool, sec_machine_address, sec_machine_username, sec_machine_password, sec_machine_rsa_ssh_key, sec_pool_name, sec_input_file, sec_exec_file, sec_config_files_path):
        
        """
        method for validating input data during sec config pool udpate process
        """
        from src.business.incident.correlation.sec.sec import SecConfigPool
        
        error = None
        
       
        config_pool = SecConfigPool.objects(sec_pool_name=sec_pool_name).first()
           
        if config_pool and str(config_pool.id) != str(id_config_pool):
            if not error: 
                error = {}
            error["name_exist_error"] = u"Ce nom existe déjà"
            
        if sec_machine_address == "":
            if not error: 
                error = {}
            error["sec_machine_address_empty_error"] = u"Vous devez spécifier une adresse IP valide"
                           
        if sec_machine_username == "":
            if not error: 
                error = {}
            error["sec_machine_username_empty_error"] = u"Vous devez spécifier un nom d'utilisateur valide pour une connexion ssh sur la machine Sec"
            
        if sec_machine_password == "":
            if not error: 
                error = {}
            error["sec_machine_password_empty_error"] = u"Vous devez spécifier un mot de passe valide pour une connexion ssh sur la machine Sec"
            
        if sec_pool_name == "":
            if not error: 
                error = {}
            error["sec_pool_name_empty_error"] = u"Vous devez spécifier un nom de pool et il doit être unique"
        
        if sec_input_file == "":
            if not error: 
                error = {}
            error["sec_input_file_empty_error"] = u"Vous devez spécifier le chemin absolu vers le fichier de données pour la corrélation"
        
        if sec_config_files_path == "":
            if not error: 
                error = {}
            error["sec_config_files_path_empty_error"] = u"Vous devez spécifier le chemin absolu du repertoire de ce pool de configuration Sec"

            
        if sec_exec_file == "":
            if not error: 
                error = {}
            error["sec_exec_file_empty_error"] = u"Vous devez spécifier le chemin absolu vers le fichier executable sec"

        if sec_machine_rsa_ssh_key == "":
            if not error: 
                error = {}
            error["sec_machine_rsa_ssh_key_empty_error"] = u"Vous devez spécifier la clé public RSA du serveur SSH de la machine sec"
   
            
        return error
    
#=============================================================================
# Configuration file logic class  

class SecConfigFileLogic:
    
    def create_config_file(self, id_config_pool, draft_config, sec_config_file):
        """This method is for registring a new Sec config file"""
        from src.business.incident.correlation.sec.sec import SecConfigFile
        from src.business.incident.correlation.sec.sec import SecConfigPool
        error = self.validate_form_create(draft_config, sec_config_file)
        res = {"error":error, "object_id":None}
        if not error:
            config_file = SecConfigFile(draft_config = draft_config, sec_config_file = sec_config_file)
            config_file.save()
            res["object_id"] = config_file.id
            conf_pool = SecConfigPool.objects(id=id_config_pool)
            conf_pool.update_one(push__config_files=config_file)
        return res
    
    def update_config_file(self,  id_config_file, draft_config, sec_config_file):
        """This method is for update a new sec config file"""
        from src.business.incident.correlation.sec.sec import SecConfigFile
        error = self.validate_form_create(draft_config, sec_config_file)
        res = {"error":error, "object_id":None}
        if not error:
            object_instance = SecConfigFile.objects(id = id_config_file).first()
            object_instance.draft_config = draft_config
            object_instance.sec_config_file = sec_config_file
            object_instance.save()
            res["object_id"] = object_instance.id
        return res
    
    def restore_config_file(self,  id_config_file):
        """This method is for restore a new sec config file"""
        from src.business.incident.correlation.sec.sec import SecConfigFile
        
        res = {"error":None, "object_id":None}
        object_instance = SecConfigFile(id = id_config_file).first()
        object_instance.draft_config = object_instance.previous_runing_config
        res["object_id"] = object_instance.id
        object_instance.save()
        
        return res
    
    def delete_config_file(self, id_config_pool, id_config_file):
        from src.business.incident.correlation.sec.sec import SecConfigFile
        from src.business.incident.correlation.sec.sec import SecConfigPool
        
        error = None
        config_pool = SecConfigPool.objects(id=id_config_pool)
        config_file = SecConfigFile.objects(id=id_config_file).first()
        
        if config_pool and config_file:
            config_pool.update_one(pull__config_files=config_file)
            config_file.delete()
        
        return error
    
    def get_config_file(self, id_config_file):
        
        from src.business.incident.correlation.sec.sec import SecConfigFile
        
        config_file = SecConfigFile.objects(id=id_config_file).first()
        
        return config_file
    
    def get_remote_config_file(self, id_config_pool, id_config_file):
        from src.business.incident.correlation.sec.sec import SecConfigFile
        from src.business.incident.correlation.sec.sec import SecConfigPool
        import paramiko, base64
        
        file_name = ""
        file_data = ""
        config_file = SecConfigFile.objects(id=id_config_file).first()
        config_pool = SecConfigPool.objects(id=id_config_pool).first()
        
        key = paramiko.RSAKey(data=base64.decodestring(config_pool.sec_machine_rsa_ssh_key))
        client = paramiko.SSHClient()
        client.get_host_keys().add(config_pool.sec_machine_address, 'ssh-rsa', key)
        client.connect(config_pool.sec_machine_address, username=config_pool.sec_machine_username, password=config_pool.sec_machine_password)
        sftp_client = client.open_sftp()
        if config_pool.sec_config_files_path[-1] == "/":
            file_name = config_pool.sec_config_files_path + config_file.sec_config_file
        else:
            file_name = config_pool.sec_config_files_path + "/" + config_file.sec_config_file
            
        remote_file = sftp_client.open(file_name)
        try:
            for line in remote_file:
                file_data = file_data+line
        finally:
            remote_file.close()
            
        return file_data
    
    def send_config_file(self, id_config_pool, id_config_file):
        from src.business.incident.correlation.sec.sec import SecConfigFile
        from src.business.incident.correlation.sec.sec import SecConfigPool
        import paramiko, base64
        error = None
        config_pool = SecConfigPool.objects(id=id_config_pool).first()
        config_file = SecConfigFile.objects(id=id_config_file).first()
        
        previous_config = self.get_remote_config_file(id_config_pool, id_config_file)
        
        key = paramiko.RSAKey(data=base64.decodestring(config_pool.sec_machine_rsa_ssh_key))
        client = paramiko.SSHClient()
        client.get_host_keys().add(config_pool.sec_machine_address, 'ssh-rsa', key)
        client.connect(config_pool.sec_machine_address, username=config_pool.sec_machine_username, password=config_pool.sec_machine_password)
        sftp_client = client.open_sftp()
        
        
        if config_pool.sec_config_files_path[-1] == "/":
            file_name = config_pool.sec_config_files_path + config_file.sec_config_file
        else:
            file_name = config_pool.sec_config_files_path + "/" + config_file.sec_config_file
            
        remote_file = sftp_client.open(file_name, "w")
        
        try:
            
            for line in config_file.draft_config:
                
                remote_file.write(line)
            
            config_file.previous_runing_config = previous_config
            config_file.save()
        finally:
            remote_file.close()
        
        
        return error
    
    def get_config_files_onConfigPool(self, id_config_pool):
        from src.business.incident.correlation.sec.sec import SecConfigPool
        
        config_pool = SecConfigPool.objects(id=id_config_pool).first()
        config_file_list = config_pool.config_files
        return config_file_list
    
    def validate_form_create(self, draft_config, sec_config_file):
        
        """
        method for validating input data during sec config file creation process
        """
        error = None
        
        if sec_config_file == "":
            if not error: 
                error = {}
            error["sec_config_file_empty_error"] = u"Le nom de fichier ne peut être vide"
            
        return error

    
    def validate_form_update(self, id_config_pool, sec_machine_address, sec_machine_username, sec_machine_password, sec_machine_rsa_ssh_key, sec_pool_name, sec_lauch_command, sec_config_path_dir, is_manual_launch):
        
        """
        method for validating input data during sec config file udpate process
        """
        return None
