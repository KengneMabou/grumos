# coding: utf-8 
'''
Created on 25 juil. 2016

@author: kengne
'''

from src.technique.application_init.settings_vars import user_profiles
from mongoengine import Document, StringField, signals


class User(Document):
    
    name = StringField(verbose_name="Name", max_length=255, required=False)
    surname = StringField(verbose_name="Surname", max_length=255, required=False)
    email = StringField(verbose_name="Email", max_length=255, required=False)
    login = StringField(verbose_name="Login", max_length=255, required=True, unique=True)
    password = StringField(verbose_name="Password", max_length=255, required=True)
    profile = StringField(default = user_profiles.get('admin'), verbose_name="Profile", max_length=255, required=True)
    call_hash = True
    @classmethod
    def pre_save(cls, sender, document, **kwargs):
        import hashlib
        if cls.call_hash:
            document.password = hashlib.sha1(document.password).hexdigest()
    
    def has_permission (self, permission_name, entity_name):
        """Check if the current user has à particular permission (permission_name) on the given entity (entity name)"""    
        if permission_name == self.profile:
            return True
       
        return False
        
        
        

signals.pre_save.connect(User.pre_save, sender=User)
