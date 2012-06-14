import pygame
import threading
import time

from bloodyhell.eventdispatcher import EventDispatcher
from bloodyhell.navigator import Navigator

class Game(object):

    FRAMES_PER_SECOND = 25
    FRAMES_MINIMUM_DELTA = 0.001

    def __init__(self, name, resolution, view_type, fps = FRAMES_PER_SECOND):
        super(Game, self).__init__()
        pygame.init()
        self._window = pygame.display.set_mode(resolution)
        pygame.display.set_caption(name) 
        self._screen = pygame.display.get_surface()
        self._frames_delta = 1.0 / Game.FRAMES_PER_SECOND
        self._navigator = Navigator(self._screen)
        self._navigator.set_current_view(view_type)

    def run(self):
        while True:
            time_reference = time.time()
            events = pygame.event.get()
            self._navigator.on_frame(self._frames_delta)
            for event in events :
                self._navigator.on_event(event)
            elapsed_time = time_reference - time.time()
            if self._frames_delta - elapsed_time >= Game.FRAMES_MINIMUM_DELTA:
                time.sleep(self._frames_delta - elapsed_time)
