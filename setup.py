'''
Created on 25 juil. 2016

@author: kengne
'''

import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "GRUMOS",
    version = "0.1",
    url = '',
    author_email = 'kmhf.legenie@gmail.com',
    license = 'AGPL',
    description = "A hypervision system for pragmatic IT manager",
    long_description = read('README'),
    author = 'Kengne Mabou',
    packages = find_packages('src'),
    package_dir = {'': 'src'},
    install_requires = ['setuptools',
                        'jinja2',
                        'flask',
                        'flask-script',
                        'WTForms',
                        'mongoengine',
                        'blinker',
                        'mongomock',
                        'tox',
                        'flask_mongoengine',
                        'paramiko',
                        'plumbum',
                        'celery',
                        'fabric',
                        'python-crontab',
                        'Celery'
                        'shell',
                        'python-nmap',
                        
                        ],
      classifiers = [
        'Development Status :: Beta',
        'Intended Audience :: IT Administrator :: IT Manager',
        'License :: OSI Approved :: AGPL License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Monitoring :: Machine Learning :: Incident detection',
    ]
)
