from bloodyhell.eventdispatcher import EventDispatcher
from bloodyhell.layer import Layer


class Navigator(EventDispatcher):

    _current_view = None

    def __init__(self):
        super(Navigator, self).__init__()
        screen_width = 1 # TO CHANGE
        screen_height = 1 # TO CHANGE
        self._root = Layer(None, (0, 0), (
            screen_width, screen_height
        ))
        self.add(self._root)
        self._stack = []

    def current_view(self):
        return self._current_view

    def push(self, view):
        if self._current_view:
            self._stack.append(self._current_view)
        self.set_current_view(view)

    def pop(self):
        if len(self._stack):
            self.set_current_view(self._stack.pop())

    def set_current_view(self, view):
        if self._current_view:
            self._root.remove_layer(self._current_view)
        self._root.add_layer(view)
        self._current_view = view
        self._current_view.set_navigator(self)

    def on_frame(self, delta):
        super(Navigator, self).on_frame(delta)
        if self._current_view:
            self._current_view
