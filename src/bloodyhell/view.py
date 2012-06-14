import pygame

from bloodyhell.layer import Layer


class View(Layer):
    
    def set_navigator(self, navigator):
        self._navigator = navigator

