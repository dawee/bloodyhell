import pygame
import threading

from bloodyhell.eventdispatcher import EventDispatcher
from bloodyhell.resourceloader import ResourceLoader

class Layer(EventDispatcher):

    def __init__(self, parent, position, size):
        super(Layer, self).__init__()
        self._parent = parent
        self._surface = pygame.Surface(size)
        self._rect = pygame.Rect(position, size)
        self._slots = {}

    def addLayer(self, position, size, layer_type=None, slot=0):
        if layer_type is None:
            layer_type = Layer
        layer = layer_type(self._surface, position, size)
        if not slot in self._slots:
            self._slots[slot] = []
        self._slots[slot].append(layer)
        self.add(layer)
        return layer

    def blit(self):
        self._parent.blit(self._surface, (self._rect.x, self._rect.y))

    def on_frame(self, delta):
        for slot in self._slots.keys():
            for layer in self._slots[slot]:
                layer.on_frame(delta)
                layer.blit()
        self.blit()

    def rect(self):
        return self._rect

    def fill(self, color):
        self._surface.fill(color)

    def set_image(self, image_id):
        self._surface = ResourceLoader().get_resource(image_id)

