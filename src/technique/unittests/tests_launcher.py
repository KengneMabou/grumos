# coding: utf-8
'''
Created on 9 août 2016

@author: kengne
'''

import sys, os , inspect
current_path = os.path.realpath(os.path.abspath(os.path.dirname(inspect.getfile( inspect.currentframe()))))
application_dir_path = current_path
#application_dir_path = os.path.join(current_path, '') #path with the ending '/'    
sys.path.insert(0, application_dir_path)

import unittest
from system.auth_test import AuthLogicTestCase
from system.user_management_test import UserMgtLogicTestCase

if __name__ == '__main__':
    unittest.main()
