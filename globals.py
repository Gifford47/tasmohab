import os
from jinja2 import Environment, FileSystemLoader

def init_jinja_environment(template_path=None):
    global jinja_environment
    base_path = os.path.dirname(__file__)       # get path of current script file
    template_path_list = []
    std_tpl_path = os.path.join(base_path, 'ohgen/templates')
    if template_path:
        template_path_list = [f.path for f in os.scandir(template_path) if f.is_dir()]
    tmp = [f.path for f in os.scandir(std_tpl_path) if f.is_dir()]      # return a list of all subdirs
    template_path_list.extend(tmp)                                      # include all subdirs of standard dir
    template_path_list.append(std_tpl_path)                             # include standard dir
    template_path_list.append(os.path.join(base_path, 'templates'))              # std template path for single exe/one-file
    template_path_list = [os.path.normpath(p) for p in template_path_list]      # normalize path strings
    jinja_environment = Environment(loader=FileSystemLoader(template_path_list))


