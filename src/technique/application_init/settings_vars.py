# -*- coding: utf-8 -*
'''
Created on 27 juil. 2016

@author: kengne
'''

session_attrs ={
                    'logged_in_attr':'looged_in',
                    'username_attr': 'username',
                    'password_attr':'password',
                    'profile_attr': 'profile',
                    'name_attr': 'name',
                    'logintime_attr': 'login_time',
                    'user_id_attr': 'user_id',
                }

user_profiles = {
                    'admin':'IT_ADMIN',
                    'manager': 'IT_MANAGER',
                    'simple_user':'IT_USER',
                    'bpo':'BPO'
                }


list_profiles = {
                    'IT_ADMIN':u'Administrateur IT',
                    'IT_MANAGER': u'Manager IT',
                    'IT_USER':u'Utilisateur IT',
                    'BPO':u'Manager de process métier'
                }

default_user = {'name':'Administrator',
                'surname':'Root',
                'email':'admin@mycompany.com',
                'login':'admin',
                'password':'admin',
                'profile':user_profiles.get('admin')
            }