import time
import Queue

from bloodyhell.view.navigator import Navigator
from bloodyhell.resourceloader import ResourceLoader
from bloodyhell.widget import Widget


class Game(object):

    FRAMES_PER_SECOND = 25
    FRAMES_MINIMUM_DELTA = 0.001

    _message_queue = Queue.Queue()

    @staticmethod
    def quit():
        Game._message_queue.put('quit')

    def __init__(self, name, resolution,
                    resources_folder, fps=FRAMES_PER_SECOND):
        super(Game, self).__init__()
        ResourceLoader().set_resources_folder(resources_folder)
        Widget.set_resolution(resolution)
        self._frames_delta = 1.0 / fps
        self._navigator = Navigator()

    def navigator(self):
        return self._navigator

    def read_message(self):
        message = None
        try:
            message = Game._message_queue.get_nowait()
        except Queue.Empty:
            message = None
        return message

    def run(self):
        while True:
            message = self.read_message()
            if message == 'quit':
                break
            time_reference = time.time()
            events = []
            self._navigator.on_frame(self._frames_delta)
            for event in events:
                self._navigator.on_event(event)
            elapsed_time = time.time() - time_reference
            if self._frames_delta - elapsed_time >= Game.FRAMES_MINIMUM_DELTA:
                time.sleep(self._frames_delta - elapsed_time)
