# coding: utf-8 
'''
Created on 3 sept. 2016
@author: kengne
'''
from mongoengine import Document, BooleanField, StringField

class MonitoringConsole(Document):
    """This class represent a monitoring console"""
    
    name = StringField(verbose_name="Name", max_length=255, required=True, unique = True)
    location = StringField(verbose_name="Location", max_length=255, required=True)
    port = StringField(verbose_name="Port", max_length=255, required=True)
    path = StringField(verbose_name="URL PATH", max_length=255, required=False)
    

class HardComponent(Document):
    
    name = StringField(verbose_name="Name", max_length=255, required=True, unique = True)
    address = StringField(verbose_name="IP address", max_length=255, required=True)
    mac = StringField(verbose_name="MAC address", max_length=255, required=True)
    isTrashed = BooleanField(verbose_name="is trashed ?", max_length=255, required=True, default =False)
    state = ""
    
    meta = {
        'strict':False,
    }
    
    def isUp(self):
        import nmap
        val = False
        nm = nmap.PortScanner()
        nm.scan(hosts=self.address, arguments="-sP")
        try:
            st = nm[self.address].state()
            if st == 'up':
                val = True
        except KeyError:
            val = False
            
        return val
    
class ServiceComponent(Document):
    name = StringField(verbose_name="Name", max_length=255, required=True, unique = True)
    description = StringField(verbose_name="Description")
    