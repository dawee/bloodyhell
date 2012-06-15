from bloodyhell.layer import Layer
from bloodyhell.resourceloader import ResourceLoader


class View(Layer):

    def __init__(self):
        super(View, self).__init__(self)
        self._loader = ResourceLoader()

    def set_navigator(self, navigator):
        self._navigator = navigator

    def loader(self):
        return self._loader