# coding: utf-8 
'''
Created on 11 sept. 2016

@author: kengne
'''

from mongoengine import Document, StringField, ReferenceField, ListField, BooleanField


class SecConfigFile(Document):
    
    draft_config = StringField(verbose_name="Draft config")
    previous_runing_config = StringField(verbose_name="Previous config")
    sec_config_file = StringField(verbose_name="Config file name only without the path", max_length=255, required=True)

class SecConfigPool(Document):
    """"
    Par défaut on lance tous les fichiers de configuration du pool
    """
    sec_machine_address = StringField(verbose_name="IP address", max_length=255, required=True)
    sec_machine_username = StringField(verbose_name="Username", max_length=255, required=True)
    sec_machine_password = StringField(verbose_name="Password", max_length=255, required=True)
    sec_machine_rsa_ssh_key = StringField(verbose_name="Clé public RSA du serveur SSH sec", required=True) 
    sec_pool_name = StringField(verbose_name="Logstash config pool name", max_length=255, required=True, unique= True)
    sec_input_file = StringField(verbose_name="Absolute path of the of data input file", max_length=255, required=True)#option --input
    sec_exec_file = StringField(verbose_name="Absolute path of the sec binary", max_length=255, required=True)
    sec_config_files_path = StringField(verbose_name="Absolute path of config directory of config file", max_length=255, required=True)#option --conf Eg: --conf /var/lib/data/*
    config_files = ListField(ReferenceField(SecConfigFile))


    
