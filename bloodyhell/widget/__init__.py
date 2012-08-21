import re
from bloodyhell.layer import Layer


class Widget(Layer):

    _screen_width = None
    _screen_height = None

    PATTERNS = {
        'percent': re.compile('^(\-*[0-9]+) *\%$'),
        'pixel': re.compile('^(\-*[0-9]+) *px$'),
        'undefined': re.compile('^(\-*[0-9]+)$'),
    }

    def __init__(self, style=None):
        super(Widget, self).__init__()
        self._style = {}

    def style(self, property, value):
        self._style[property] = value

    def read_value(self, raw_value):
        for name, pattern in Widget.PATTERNS.items():
            result = pattern.match(raw_value)
            if result:
                return (name, result.group(1))

    def _update_size(self):
        if 'width' in self._style:
            parent_value = Widget._screen_width
            if self._parent is not None:
                parent_value = self._parent._rect.width
            pattern_name, value = self.read_value(self._style['width'])
            if pattern_name == 'percent':
                self._rect.width = value * parent_value / 100
            else:
                self._rect.width = value
        if 'height' in self._style:
            parent_value = Widget._screen_height
            if self._parent is not None:
                parent_value = self._parent._rect.height
            pattern_name, value = self.read_value(self._style['height'])
            if pattern_name == 'percent':
                self._rect.height = value * parent_value / 100
            else:
                self._rect.height = value

    def _update_x_position(self):
        parent_width = Widget._screen_width
        if self._parent is not None:
            parent_width = self._parent._rect.width

        if 'left' in self._style:
            parent_value = 0
            if self._parent is not None:
                parent_value = self._parent._rect.left
            pattern_name, value = self.read_value(self._style['left'])
            if pattern_name == 'percent':
                self._rect.left = parent_value + (value * parent_width / 100)
            else:
                self._rect.left = parent_value + value

        if 'right' in self._style:
            parent_value = Widget._screen_width
            if self._parent is not None:
                parent_value = self._parent._rect.right
            pattern_name, value = self.read_value(self._style['right'])
            if pattern_name == 'percent':
                self._rect.right = parent_value - (value * parent_width / 100)
            else:
                self._rect.right = parent_value - value

    def _update_y_position(self):
        parent_height = Widget._screen_height
        if self._parent is not None:
            parent_height = self._parent._rect.height

        if 'top' in self._style:
            parent_value = 0
            if self._parent is not None:
                parent_value = self._parent._rect.top
            pattern_name, value = self.read_value(self._style['top'])
            if pattern_name == 'percent':
                self._rect.top = parent_value + (value * parent_height / 100)
            else:
                self._rect.top = parent_value + value

        if 'bottom' in self._style:
            parent_value = Widget._screen_height
            if self._parent is not None:
                parent_value = self._parent._rect.bottom
            pattern_name, value = self.read_value(self._style['bottom'])
            if pattern_name == 'percent':
                self._rect.bottom = parent_value - (value * parent_height / 100)
            else:
                self._rect.bottom = parent_value - value

    def on_frame(self, delta):
        self._update_size()
        self._update_x_position()
        self._update_y_position()
        super(Widget, self).on_frame(delta)

    @staticmethod
    def set_resolution(self, resolution):
        Widget._screen_width, Widget._screen_height = resolution
