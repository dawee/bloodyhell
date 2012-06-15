from bloodyhell.layer import Layer

class Chunk(object):

    def __init__(self, position, size):
        self._camera = None
        self._layer = Layer()
        self._position = position
        self._size = size

    def set_camera(self, camera):
        self._camera = camera

    def update_rect(self):
        if self._camera:
            self._camera.set_layer_rect(
                self._layer, self._position, self._size
            )

    def layer(self):
        return self._layer