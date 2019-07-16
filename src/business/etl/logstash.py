# coding: utf-8 
'''
Created on 11 sept. 2016

@author: kengne
'''

from mongoengine import Document, ReferenceField, StringField, ListField, BooleanField


class LogstashConfigFile(Document):
    
    draft_config = StringField(verbose_name="Draft config")
    previous_runing_config = StringField(verbose_name="Previous config")
    etl_config_file = StringField(verbose_name="Config file name only without the path", max_length=255, required=True)
    
class LogstashConfigPool(Document):
    
    etl_machine_address = StringField(verbose_name="IP address", max_length=255, required=True)
    etl_machine_username = StringField(verbose_name="Username", max_length=255, required=True)
    etl_machine_password = StringField(verbose_name="Password", max_length=255, required=True)
    etl_machine_rsa_ssh_key = StringField(verbose_name="Clé public RSA du serveur SSH logstash", required=True)
    etl_pool_name = StringField(verbose_name="Logstash config pool name", max_length=255, required=True, unique= True)
    etl_lauch_command = StringField(verbose_name="Logstash launch command", max_length=255)
    etl_config_path_dir = StringField(verbose_name="Config directory", max_length=255, required=True)
    is_manual_launch = BooleanField(verbose_name="Call the launch command as if it where the the binary logstash command with -f option",default=False)
    config_files = ListField(ReferenceField(LogstashConfigFile))
    
    