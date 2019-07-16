'''
Created on 26 juil. 2016

@author: kengne
'''

from flask import Blueprint, send_from_directory
from flask.views import MethodView


static_url_register = Blueprint('static_urls', __name__)

class SendPluginsView(MethodView):

    def get(self, path):
        
        return send_from_directory('../src/view/web_assets/templates/admin_lte/plugins/', path)


    
class SendBootstrapView(MethodView):

    def get(self, path):
        
        return send_from_directory('../src/view/web_assets/templates/admin_lte/bootstrap/', path)


    
class SendDistView(MethodView):

    def get(self, path):
        
        return send_from_directory('../src/view/web_assets/templates/admin_lte/dist/', path)

class SendImagesView(MethodView):

    def get(self, path):
        
        return send_from_directory('../src/view/web_assets/images/', path)

class SendJavascriptView(MethodView):

    def get(self, path):
        
        return send_from_directory('../src/view/web_assets/javascripts/', path)

class SendCssView(MethodView):

    def get(self, path):
        
        return send_from_directory('../src/view/web_assets/css/', path)
    

# Register the urls
static_url_register.add_url_rule('/plugins/<path:path>', view_func=SendPluginsView.as_view('send_plugins_handler'))
static_url_register.add_url_rule('/bootstrap/<path:path>', view_func=SendBootstrapView.as_view('send_bootstrap_handler'))
static_url_register.add_url_rule('/dist/<path:path>', view_func=SendDistView.as_view('send_dist_handler'))
static_url_register.add_url_rule('/images/<path:path>', view_func=SendImagesView.as_view('send_images_handler'))
static_url_register.add_url_rule('/javascripts/<path:path>', view_func=SendJavascriptView.as_view('send_javascript_handler'))
static_url_register.add_url_rule('/css/<path:path>', view_func=SendCssView.as_view('send_css_handler'))