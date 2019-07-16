# coding: utf-8
'''
Created on 13 sept. 2016

@author: kengne
'''
class LogstashConfigPoolLogic:
    
    
    config_pool = None
    
    
    def start_config_pool(self, id_config_pool):
        
        import paramiko, base64, time
        
        stdin = ""
        stdout = "" 
        stderr = ""
        msg = list()
        cpt = 0
        
        #base64_server_rsa_ssh_key = "AAAAB3NzaC1yc2EAAAADAQABAAABAQC5r2S0u0ho5ZPVnp+gDdUszrsyyK1x1Rfw7i6wa2bPNjUn9msvbWfyXT8A/o2AZGiQzJuhCbH4x3jLQVsgmrThqFdStPpddwdNCutHKSSlljoe0XitUt+NxdImBKwuamNWnABEvHNvTTJtDEwd4oz4PDEU74afVtjarmevdVJVDJEPPeHw6jsBhjs+bOV6S8FAbBD5HkWw1FBl/2AZIT64bUrW/c62eNp8kGFLiDE9ck/d+vCPL/SU/Wtojv0d9qtH21Uv+NEBcWDDxdQIi8g7YuZRtLpi3XOlxdU5JaRARJONVuhTjA35gZXFZXQhLaKieytr89z8aNMblS6VJWWz"
        config_pool = self.get_config_pool(id_config_pool)
        key = paramiko.RSAKey(data=base64.decodestring(config_pool.etl_machine_rsa_ssh_key))
        client = paramiko.SSHClient()
        client.get_host_keys().add(config_pool.etl_machine_address, 'ssh-rsa', key)
        client.connect(config_pool.etl_machine_address, username=config_pool.etl_machine_username, password=config_pool.etl_machine_password)
        
        pid_file = 'pid'+time.time()+".pid"
        log_file = 'log'+time.time()+".log"
        
        if config_pool.is_manual_launch:
            stdin, stdout, stderr = client.exec_command("nohup "+config_pool.etl_lauch_command+" --debug --auto-reload --allow_unsafe_shutdown -f "+config_pool.etl_config_path_dir+" --log "+log_file+" >/dev/null 2>&1 &")
        else:
            stdin, stdout, stderr = client.exec_command(config_pool.etl_lauch_command)
        
        for line in stdout:
            cpt = cpt + 1
            msg.append(''+line.strip('\n'))
            time.sleep(1)
            if cpt == 4:
                break
                
            
        
        return msg
        

    def delete_config_pool(self, id_config_pool):
        from src.business.etl.logstash import LogstashConfigPool
        
        error = None
        config_pool = LogstashConfigPool.objects(id=id_config_pool).first()
        
        if config_pool :
            config_pool.delete()
        
        return error
    

    def get_config_pool(self, id_config_pool):
        from src.business.etl.logstash import LogstashConfigPool
        
        config_pool = LogstashConfigPool.objects(id=id_config_pool).first()
        
        return config_pool
          
    def list_config_pools(self):
        from src.business.etl.logstash import LogstashConfigPool
        
        config_pools = LogstashConfigPool.objects.all()
        
        return config_pools


    def update_config_pool(self, id_config_pool, etl_machine_address, etl_machine_username, etl_machine_password, etl_machine_rsa_ssh_key, etl_pool_name, etl_lauch_command, etl_config_path_dir, is_manual_launch):
        """
            Method for updating infos about a logstash config pool
        """
        from src.business.etl.logstash import LogstashConfigPool
        
       
        error = self.validate_form_update(id_config_pool, etl_machine_address, etl_machine_username, etl_machine_password, etl_machine_rsa_ssh_key, etl_pool_name, etl_lauch_command, etl_config_path_dir, is_manual_launch)
        
        if not error:
            config_pool =  LogstashConfigPool.objects(id=id_config_pool).first()
            config_pool.etl_machine_address = etl_machine_address
            config_pool.etl_machine_username = etl_machine_username
            config_pool.etl_machine_password = etl_machine_password
            config_pool.etl_machine_rsa_ssh_key = etl_machine_rsa_ssh_key
            config_pool.etl_pool_name = etl_pool_name
            config_pool.etl_lauch_command = etl_lauch_command
            config_pool.etl_config_path_dir = etl_config_path_dir
            config_pool.is_manual_launch = is_manual_launch
            config_pool.save()
        return error
    
    def create_config_pool(self, etl_machine_address, etl_machine_username, etl_machine_password, etl_machine_rsa_ssh_key, etl_pool_name, etl_lauch_command, etl_config_path_dir, is_manual_launch):
        """This method is for registring a new logstash pool"""
        from src.business.etl.logstash import LogstashConfigPool
        error = self.validate_form_create(etl_machine_address, etl_machine_username, etl_machine_password, etl_machine_rsa_ssh_key, etl_pool_name, etl_lauch_command, etl_config_path_dir, is_manual_launch)
        if not error:
            LogstashConfigPool(etl_machine_address = etl_machine_address , etl_machine_username = etl_machine_username, etl_machine_password = etl_machine_password, etl_machine_rsa_ssh_key = etl_machine_rsa_ssh_key, etl_pool_name = etl_pool_name, etl_lauch_command = etl_lauch_command, etl_config_path_dir = etl_config_path_dir, is_manual_launch = is_manual_launch).save()
        return error
        
    def validate_form_create(self, etl_machine_address, etl_machine_username, etl_machine_password, etl_machine_rsa_ssh_key, etl_pool_name, etl_lauch_command, etl_config_path_dir, is_manual_launch):
        
        """
        method for validating input data during logstash config pool creation process
        """
        from src.business.etl.logstash import LogstashConfigPool
        
        error = None
        
            
        config_pool = LogstashConfigPool.objects(etl_pool_name=etl_pool_name).first()
        
        if config_pool:
            if not error: 
                error = {}
            error["etl_pool_name_exist_error"] = u"Ce nom de pool existe déjà"
            
        if etl_machine_address == "":
            if not error: 
                error = {}
            error["etl_machine_address_empty_error"] = u"Vous devez spécifier une adresse IP valide"
                           
        if etl_machine_username == "":
            if not error: 
                error = {}
            error["etl_machine_username_empty_error"] = u"Vous devez spécifier un nom d'utilisateur valide pour une connexion ssh sur la machine Logstash"
            
        if etl_machine_password == "":
            if not error: 
                error = {}
            error["etl_machine_password_empty_error"] = u"Vous devez spécifier un mot de passe valide pour une connexion ssh sur la machine Logstash"
            
        if etl_pool_name == "":
            if not error: 
                error = {}
            error["etl_pool_name_empty_error"] = u"Vous devez spécifier un nom de pool et il doit être unique"
        
        if etl_lauch_command == "":
            if not error: 
                error = {}
            error["etl_lauch_command_empty_error"] = u"Vous devez spécifier la commande de lancement de Logstash"
            
        if etl_config_path_dir == "":
            if not error: 
                error = {}
            error["etl_config_path_dir_empty_error"] = u"Vous devez spécifier le chemin de repertoire de ce pool de configuration Logstash"
            
        if etl_machine_rsa_ssh_key == "":
            if not error: 
                error = {}
            error["etl_machine_rsa_ssh_key_empty_error"] = u"Vous devez spécifier la clé public RSA du serveur SSH de la machine logstash"

            
            
        return error
    
    def validate_form_update(self, id_config_pool, etl_machine_address, etl_machine_username, etl_machine_password, etl_machine_rsa_ssh_key, etl_pool_name, etl_lauch_command, etl_config_path_dir, is_manual_launch):
        
        """
        method for validating input data during logstash config pool udpate process
        """
        from src.business.etl.logstash import LogstashConfigPool
        
        error = None
        
       
        config_pool = LogstashConfigPool.objects(etl_pool_name=etl_pool_name).first()
           
        if config_pool and str(config_pool.id) != str(id_config_pool):
            if not error: 
                error = {}
            error["name_exist_error"] = u"Ce nom existe déjà"
            
        if etl_machine_address == "":
            if not error: 
                error = {}
            error["etl_machine_address_empty_error"] = u"Vous devez spécifier une adresse IP valide"
                           
        if etl_machine_username == "":
            if not error: 
                error = {}
            error["etl_machine_username_empty_error"] = u"Vous devez spécifier un nom d'utilisateur valide pour une connexion ssh sur la machine Logstash"
            
        if etl_machine_password == "":
            if not error: 
                error = {}
            error["etl_machine_password_empty_error"] = u"Vous devez spécifier un mot de passe valide pour une connexion ssh sur la machine Logstash"
            
        if etl_pool_name == "":
            if not error: 
                error = {}
            error["etl_pool_name_empty_error"] = u"Vous devez spécifier un nom de pool et il doit être unique"
        
        if etl_lauch_command == "":
            if not error: 
                error = {}
            error["etl_launch_command_empty_error"] = u"Vous devez spécifier la commande de lancement de Logstash"
            
        if etl_config_path_dir == "":
            if not error: 
                error = {}
            error["etl_config_path_dir_empty_error"] = u"Vous devez spécifier le chemin de repertoire de ce pool de configuration Logstash"

        if etl_machine_rsa_ssh_key == "":
            if not error: 
                error = {}
            error["etl_machine_rsa_ssh_key_empty_error"] = u"Vous devez spécifier la clé public RSA du serveur SSH de la machine logstash"
   
            
        return error
    
#=============================================================================
# Configuration file logic class  

class LogstashConfigFileLogic:
    
    def create_config_file(self, id_config_pool, draft_config, etl_config_file):
        """This method is for registring a new logstash config file"""
        from src.business.etl.logstash import LogstashConfigFile
        from src.business.etl.logstash import LogstashConfigPool
        error = self.validate_form_create(draft_config, etl_config_file)
        res = {"error":error, "object_id":None}
        if not error:
            config_file = LogstashConfigFile(draft_config = draft_config, etl_config_file = etl_config_file)
            config_file.save()
            res["object_id"] = config_file.id
            conf_pool = LogstashConfigPool.objects(id=id_config_pool)
            conf_pool.update_one(push__config_files=config_file)
        return res
    
    def update_config_file(self,  id_config_file, draft_config, etl_config_file):
        """This method is for update a new logstash config file"""
        from src.business.etl.logstash import LogstashConfigFile
        error = self.validate_form_create(draft_config, etl_config_file)
        res = {"error":error, "object_id":None}
        if not error:
            object_instance = LogstashConfigFile.objects(id = id_config_file).first()
            object_instance.draft_config = draft_config
            object_instance.etl_config_file = etl_config_file
            object_instance.save()
            res["object_id"] = object_instance.id
        return res
    
    def restore_config_file(self,  id_config_file):
        """This method is for restore a new logstash config file"""
        from src.business.etl.logstash import LogstashConfigFile
        
        res = {"error":None, "object_id":None}
        object_instance = LogstashConfigFile.objects(id = id_config_file).first()
        object_instance.draft_config = object_instance.previous_runing_config
        res["object_id"] = object_instance.id
        object_instance.save()
        
        return res
    
    def delete_config_file(self, id_config_pool, id_config_file):
        from src.business.etl.logstash import LogstashConfigPool
        from src.business.etl.logstash import LogstashConfigFile
        
        error = None
        config_pool = LogstashConfigPool.objects(id=id_config_pool)
        config_file = LogstashConfigFile.objects(id=id_config_file).first()
        
        if config_pool and config_file:
            config_pool.update_one(pull__config_files=config_file)
            config_file.delete()
        
        return error
    
    def get_config_file(self, id_config_file):
        from src.business.etl.logstash import LogstashConfigFile
        
        config_file = LogstashConfigFile.objects(id=id_config_file).first()
        
        return config_file
    
    def get_remote_config_file(self, id_config_pool, id_config_file):
        from src.business.etl.logstash import LogstashConfigFile
        from src.business.etl.logstash import LogstashConfigPool
        import paramiko, base64
        
        file_name = ""
        file_data = ""
        config_file = LogstashConfigFile.objects(id=id_config_file).first()
        config_pool = LogstashConfigPool.objects(id=id_config_pool).first()
        
        key = paramiko.RSAKey(data=base64.decodestring(config_pool.etl_machine_rsa_ssh_key))
        client = paramiko.SSHClient()
        client.get_host_keys().add(config_pool.etl_machine_address, 'ssh-rsa', key)
        client.connect(config_pool.etl_machine_address, username=config_pool.etl_machine_username, password=config_pool.etl_machine_password)
        sftp_client = client.open_sftp()
        if config_pool.etl_config_path_dir[-1] == "/":
            file_name = config_pool.etl_config_path_dir + config_file.etl_config_file
        else:
            file_name = config_pool.etl_config_path_dir + "/" + config_file.etl_config_file
            
        remote_file = sftp_client.open(file_name)
        try:
            for line in remote_file:
                file_data = file_data+line
        finally:
            remote_file.close()  
        return file_data
    
    def send_config_file(self, id_config_pool, id_config_file):
        from src.business.etl.logstash import LogstashConfigPool
        from src.business.etl.logstash import LogstashConfigFile
        import paramiko, base64
        error = None
        config_pool = LogstashConfigPool.objects(id=id_config_pool).first()
        config_file = LogstashConfigFile.objects(id=id_config_file).first()
        
        previous_config = self.get_remote_config_file(id_config_pool, id_config_file)
        
        key = paramiko.RSAKey(data=base64.decodestring(config_pool.etl_machine_rsa_ssh_key))
        client = paramiko.SSHClient()
        client.get_host_keys().add(config_pool.etl_machine_address, 'ssh-rsa', key)
        client.connect(config_pool.etl_machine_address, username=config_pool.etl_machine_username, password=config_pool.etl_machine_password)
        sftp_client = client.open_sftp()
        
        
        if config_pool.etl_config_path_dir[-1] == "/":
            file_name = config_pool.etl_config_path_dir + config_file.etl_config_file
        else:
            file_name = config_pool.etl_config_path_dir + "/" + config_file.etl_config_file
            
        remote_file = sftp_client.open(file_name, "w")
        
        try:
            
            for line in config_file.draft_config:
                
                remote_file.write(line)
            
            config_file.previous_runing_config = previous_config
            #print config_file.previous_runing_config
            config_file.save()
        finally:
            remote_file.close()
        
        
        return error
    
    def get_config_files_onConfigPool(self, id_config_pool):
        from src.business.etl.logstash import LogstashConfigPool
        
        config_pool = LogstashConfigPool.objects(id=id_config_pool).first()
        config_file_list = config_pool.config_files
        return config_file_list
    
    def validate_form_create(self, draft_config, etl_config_file):
        
        """
        method for validating input data during logstash config file creation process
        """
        error = None
        
        if etl_config_file == "":
            if not error: 
                error = {}
            error["etl_config_file_empty_error"] = u"Le nom de fichier ne peut être vide"
            
        return error

    
    def validate_form_update(self, id_config_pool, etl_machine_address, etl_machine_username, etl_machine_password, etl_machine_rsa_ssh_key, etl_pool_name, etl_lauch_command, etl_config_path_dir, is_manual_launch):
        
        """
        method for validating input data during logstash config file udpate process
        """
        return None
