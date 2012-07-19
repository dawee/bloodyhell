import pygame

from bloodyhell.eventdispatcher import EventDispatcher
from bloodyhell.layer import Layer


class Navigator(EventDispatcher):

    _current_view = None

    def __init__(self):
        super(Navigator, self).__init__()
        self._screen = pygame.display.get_surface()
        self._root = Layer(None, (0, 0), (
            self._screen.get_width(), self._screen.get_height()
        ))
        self.add(self._root)

    def set_current_view(self, view):
        self._root.addLayer(view)
        self._current_view = view
        self._current_view.set_navigator(self)

    def on_frame(self, delta):
        super(Navigator, self).on_frame(delta)
        pygame.display.flip()
