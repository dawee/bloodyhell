import pygame
import threading

from bloodyhell.eventdispatcher import EventDispatcher
from bloodyhell.resourceloader import ResourceLoader

class Layer(EventDispatcher):

    def __init__(self, parent=None, position=(0, 0), size=(0, 0)):
        super(Layer, self).__init__()
        self._parent = parent
        self._surface = pygame.Surface(size)
        self._rect = pygame.Rect(position, size)
        self._slots = {}
        self._screen = pygame.display.get_surface()

    def addLayer(self, layer, slot=0):
        if not slot in self._slots:
            self._slots[slot] = []
        layer.set_parent(self)
        self._slots[slot].append(layer)
        self.add(layer)

    def set_parent(self, parent):
        self._parent = parent

    def surface(self):
        return self._surface

    def blit(self):
        if self._parent is not None:
            self._screen.blit(
                self._surface, (
                    self._parent.rect().x + self._rect.x,
                    self._parent.rect().y + self._rect.y
                )
            )
        else:
            self._screen.blit(
                self._surface, (self._rect.x, self._rect.y)
            )

    def on_frame(self, delta):
        self.blit()
        for slot in self._slots.keys():
            for layer in self._slots[slot]:
                layer.on_frame(delta)

    def rect(self):
        return self._rect

    def set_image(self, image_id):
        self._surface = ResourceLoader().get_resource(image_id)
        self._rect = pygame.Rect(
            (self._rect.x, self._rect.y), self._surface.get_size()
        )

