# coding: utf-8 
'''
Created on 25 juil. 2016

@author: kengne

'''

from mongoengine import connect

db = connect('grumos', username='',password='',host='172.16.0.101', connect=False)

#db = connect('grumos', username='',password='',host='192.168.1.184')
#db = connect('grumos', username='',password='',host='192.168.43.155')