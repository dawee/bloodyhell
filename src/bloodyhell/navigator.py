import pygame

from bloodyhell.eventdispatcher import EventDispatcher
from bloodyhell.layer import Layer


class Navigator(EventDispatcher):

    _current_view = None

    def __init__(self, screen):
        super(Navigator, self).__init__()
        self._root = Layer(screen, (0, 0), (
            screen.get_width(), screen.get_height()
        ))
        self.add(self._root)

    def set_current_view(self, view_type):
        self._current_view = self._root.addLayer((0, 0), (
            self._root.rect().width,
            self._root.rect().height
        ), view_type)
        self._current_view.set_navigator(self)

    def on_frame(self, delta):
        super(Navigator, self).on_frame(delta)
        pygame.display.flip()
