## ! DO NOT MANUALLY INVOKE THIS setup.py, USE CATKIN INSTEAD                   

from setuptools import setup
from catkin_pkg.python_setup import generate_distutils_setup

d = generate_distutils_setup()

d['name'] = "pc_scene_completion_client"
d['description'] = "Python ROS client code for scene completion"
d['packages'] = ['pc_scene_completion_client']
d['package_dir'] = {'': 'src'}

setup(**d)
