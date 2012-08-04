import os
import sys

if not hasattr(sys, 'frozen'):
    APP_DIR = os.path.dirname(__file__)
else:
    APP_DIR = os.path.dirname(os.path.abspath(sys.executable))

sys.path.append(os.path.abspath(
    os.path.join(APP_DIR, '..', '..')
))


from distutils.core import setup
import py2exe

setup(console=['platform.py'])
