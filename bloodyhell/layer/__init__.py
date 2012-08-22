import pygame

from bloodyhell.eventdispatcher import EventDispatcher
from bloodyhell.resourceloader import ResourceLoader
from bloodyhell.layer.rect import Rect


class Layer(EventDispatcher):

    def __init__(self, parent=None, position=(0, 0), size=(0, 0)):
        super(Layer, self).__init__()
        self._parent = parent
        self._screen = pygame.display.get_surface()
        self._surface = pygame.Surface(size)
        self._rect = Rect(position, size)
        self._cropped_rect = Rect((0, 0), size)
        self._slots = {}
        self._image_id = None
        self._transparent = False

    def set_transparent(self, transparent):
        self._transparent = transparent

    def loader(self):
        return ResourceLoader()

    def add_layer(self, layer, slot=0):
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
        if self._cropped_rect is not None:
            if self._image_id is not None:
                self._surface = ResourceLoader().get_resource(
                    self._image_id, self._rect, self._cropped_rect
                )
            if self._parent is not None:
                self._screen.blit(self._surface, (
                    self._parent.rect().x + self._rect.x + self._cropped_rect.x,
                    self._parent.rect().y + self._rect.y + self._cropped_rect.y
                ))
            else:
                self._screen.blit(
                    self._surface, (self._rect.x, self._rect.y)
                )

    def on_frame(self, delta):
        if not self._transparent:
            self.blit()
        for slot in self._slots.keys():
            for layer in self._slots[slot]:
                layer.on_frame(delta)

    def rect(self):
        return self._rect

    def set_cropped_rect(self, cropped_rect):
        self._cropped_rect = cropped_rect

    def set_image(self, image_id):
        self._image_id = image_id

    def fill(self, hexcolor):
        hexcolor = hexcolor.replace('#', '')
        self._surface.fill((
            int(hexcolor[0:2], 16),
            int(hexcolor[2:4], 16),
            int(hexcolor[4:6], 16),
        ))
        return self
