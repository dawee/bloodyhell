from bloodyhell.layer.animatedlayer import AnimatedLayer
from bloodyhell.eventdispatcher import EventDispatcher

class Chunk(EventDispatcher):

    def __init__(self, position, size):
        super(Chunk, self).__init__()
        self._camera = None
        self._layer = AnimatedLayer()
        self._position = position
        self._size = size
        self._body = None
        self._geometry = None

    def append_to_world(self, world, space):
        pass

    def set_camera(self, camera):
        self._camera = camera

    def update_rect(self):
        if self._geometry is not None:
            x, y, z = self._geometry.getPosition()
            self._position = (x, y)
        if self._camera:
            self._camera.set_layer_rect(
                self._layer, self._position, self._size
            )

    def layer(self):
        return self._layer

    def set_position(self, position):
        self._position = position
        if self._geometry is not None:
            x, y = position
            self._geometry.setPosition((x, y, -0.5))

