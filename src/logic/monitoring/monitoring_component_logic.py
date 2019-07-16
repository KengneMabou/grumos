# coding: utf-8 
'''
Created on 4 sept. 2016

@author: kengne
'''
from mongoengine import Q
import os

class MonitoringComponentLogic:
    
    def list_machines(self):
        
        from src.business.monitoring.monitoring import HardComponent
        
        l_machines = HardComponent.objects.distinct("name")
        
        return l_machines
    

    def delete_hard_component(self, id_component):
        """method for deleting hardware component"""
        from src.business.monitoring.monitoring import HardComponent
        
        error = None
        component = HardComponent.objects(id=id_component).first()
        
        if component :
            component.delete()
        
        return error
    
    def trash_hard_component(self, id_component):
        """method for deleting hardware component"""
        from src.business.monitoring.monitoring import HardComponent
        
        error = None
        component = HardComponent.objects(id=id_component).first()
        
        if component :
            component.isTrashed = True
            component.save()
        
        return error
    
    def restore_hard_component(self, id_component):
        """method for deleting hardware component"""
        from src.business.monitoring.monitoring import HardComponent
        
        error = None
        component = HardComponent.objects(id=id_component).first()
        
        if component :
            component.isTrashed = False
            component.save()
        
        return error

    def get_hard_component(self, id_component):
        """method for getting a single hardware component given his id"""
        from src.business.monitoring.monitoring import HardComponent
        
        component = HardComponent.objects(id=id_component).first()
        
        return component
        
    def get_trashed_hcomponents(self):
        """method for getting a single hardware component given his id"""
        from src.business.monitoring.monitoring import HardComponent
        
        components = HardComponent.objects(Q(isTrashed=True))
        for comp in components:
            
            comp.state = "DOWN"
        
        return components
    
    def get_non_trashed_hcomponents(self):
        """method for getting a single hardware component given his id"""
        from src.business.monitoring.monitoring import HardComponent
        
        components = HardComponent.objects(Q(isTrashed=False))
        
        for comp in components:
            if comp.isUp():
                comp.state = "UP"
            else:
                comp.state = "DOWN"
        
        return components
          
    def list_hard_component(self):
        from src.business.monitoring.monitoring import HardComponent
        
        components = HardComponent.objects.all()
        
        return components


    def update_hard_component(self, id_component, name, address):
        """
            Method for updating infos about a hardware component to monitor
        """
        from src.business.monitoring.monitoring import HardComponent
        
        error = self.validate_form_create(name, address)
        
        if not error:
            component =  HardComponent.objects(id=id_component).first()
            component.name = name
            component.address = address
            component.save()
        return error
    
    def create_hard_component(self,_name, _address):
        """This method is for registring a new hardware component to monitor"""
        from src.business.monitoring.monitoring import HardComponent
        error = self.validate_form_create(_name, _address)
        if not error:
            HardComponent(name = _name, address = _address).save()
        
        return error
    
    def discover_hard_components(self, ip_range = None):
        """This method is for automatically discover new hardware component to monitor"""
        # par défaut la découverte est lancé sur le sous réseau sur lequel est branché la machine hébergeant grumos
        # Lors de l'affichage des composants découvert, on proposera un mini formulaire permettant à un utilisateur d'entrer lplage ou le sous réseau de recherche qui l'intéresse
        # on ne stocke en session et affiche uniquement les composant découvert qui n'ont pas encore été insrit en BD. A chaque appel
        # à cette methode, on vide d'abord le contenu de la session qui stocke les machines découverte
        import netifaces as ni
        import netaddr as na
    
        components = {}
        
        
        if ip_range is None or ip_range == "":
            local_ifaces_manes = ni.interfaces()
            for iface in local_ifaces_manes:
                ip_addr_infos = ni.ifaddresses(iface)
                if ni.AF_INET in ip_addr_infos and "br" not in iface and "lo" not in iface:
                    ip_netm = ip_addr_infos[ni.AF_INET][0]['addr']+"/"+ip_addr_infos[ni.AF_INET][0]['netmask']
                    ip = na.IPNetwork(ip_netm)
                    ip_cidr = str(na.IPNetwork(str(ip_addr_infos[ni.AF_INET][0]['addr'])+"/"+str(ip.prefixlen)).cidr)
                    components.update(self.scan(ip_cidr))
        else:
            components.update(self.scan(ip_range))
            
        
        return components
    
    def naive_scan(self, ip_range):
        import ipaddress
        from src.business.monitoring.monitoring import HardComponent
        components = {}
        ip_range = unicode(ip_range, "utf-8")
        ip_net = ipaddress.ip_network(ip_range)

        # Get all hosts on that network
        all_hosts = list(ip_net.hosts())
        for host in all_hosts:
            ip_addr = str(host)
            response = os.system("ping -c 1 " + ip_addr)
            if response == 0:
                hostname = ip_addr+"-hostname"
                components[hostname] = {}
                components[hostname]["name"] = hostname
                components[hostname]["address"] = ip_addr
                hcomp = HardComponent.objects(name=hostname).first()
                if hcomp:
                    components[hostname]["is_in_db"] = True
                else:
                    components[hostname]["is_in_db"] = False
                
        return components
               
                
    def scan(self, ip_range):
        from src.business.monitoring.monitoring import HardComponent
        import nmap
        components = {}
        nm = nmap.PortScanner()
        nm.scan(hosts=ip_range, arguments="-sP")
        hosts = nm.all_hosts()
        for host in hosts:
            print "Machine Grumos"+host 
            print nm[host]
            hostname = host+nm[host].hostname()
            if nm[host].hostname() == "":
                hostname = hostname+"-machine"
            #hostname = unicode(hostname, "utf-8")
            components[hostname] = {}
            components[hostname]["name"] = hostname
            components[hostname]["address"] = host
            
            if 'mac' in nm[host]['addresses']:
                components[hostname]["mac"] = nm[host]['addresses']['mac']
            else:
                components[hostname]["mac"] = ""
            
            hcomp = HardComponent.objects(mac=components[hostname]["mac"]).first()
            if hcomp:
                hcomp.address = host
                hcomp.save()
                components[hostname]["is_in_db"] = True
            else:
                components[hostname]["is_in_db"] = False
                
        return components
    
    def add_discovered_hcomponents(self, ref_component):
        """This method is for adding discovered hosts to monitoring assests"""
        from src.business.monitoring.monitoring import HardComponent
        from flask import session
        
        data = session["network_scan_results"]
        
        component = data[ref_component]
        
        HardComponent(name = component['name'], address = component['address'], mac =  component['mac']).save()
        
        data[ref_component]["is_in_db"] = True
        session.modified = True
        #print data[ref_component]
        #print data
        
        
    def validate_form_create(self, _name, _address):
        
        """
        method for validating input data during hardware component creation process
        """
        from src.business.monitoring.monitoring import HardComponent
        
        error = None
        
            
        component =HardComponent.objects(name=_name).first()
        
        if component:
            if not error: 
                error = {}
            error["name_exist_error"] = u"Ce nom existe déjà"
            
        if _name == "":
            if not error: 
                error = {}
            error["name_empty_error"] = u"Le nom du composant à monitorer est obligatoire"
               
        
            
        if _address == "":
            if not error: 
                error = {}
            error["location_empty _error"] = u"l'adresse du composant à monitorer est obligatoire"
            
            
        return error
    
    def validate_form_update(self, id_component, _name, _address):
        
        """
        method for validating input data during hard component udpate process
        """
        from src.business.monitoring.monitoring import HardComponent

        error = None
        
            
        component =HardComponent.objects(name=_name).first()
        
        if component and str(component.id) != str(id_component):
            if not error: 
                error = {}
            error["name_exist_error"] = u"Ce nom existe déjà"
            
        if _name == "":
            if not error: 
                error = {}
            error["name_empty_error"] = u"Le nom du composant à monitorer est obligatoire"
               
        
            
        if _address == "":
            if not error: 
                error = {}
            error["location_empty _error"] = u"l'adresse du composant à monitorer est obligatoire"
            
            
        return error
    
    def list_mac_addresses(self):
        
        from src.business.monitoring.monitoring import HardComponent
        
        l_mac = HardComponent.objects.distinct("mac")
        
        return l_mac
