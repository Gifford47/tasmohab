import os
from jinja2 import Environment, FileSystemLoader

def init_jinja_environment(file):
    global jinja_environment
    base_path = os.path.dirname(file)
    templ_path = os.path.join(base_path, 'ohgen/templates').replace('\\', '/')
    jinja_environment = Environment(loader=FileSystemLoader(templ_path))
