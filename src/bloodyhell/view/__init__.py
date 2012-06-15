import pygame

from bloodyhell.layer import Layer
from bloodyhell.resourceloader import ResourceLoader

class View(Layer):
    
    def set_navigator(self, navigator):
        self._navigator = navigator

    def load_package(self, package_name):
        ResourceLoader().load_package(package_name)
