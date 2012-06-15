import ode
from bloodyhell.world.chunk import Chunk


class Stence(Chunk):

    def __init__(self, resource_id, default_animation, position, size):
        super(Stence, self).__init__(position, size)
        self._resource_id = resource_id
        self.loop(default_animation)

    def append_to_world(self, world, space):
        width, height = self._size
        self._geometry = ode.GeomBox(space, lengths=(width, height, 1))
        x, y = self._position
        self._geometry.setPosition((x, y, -0.5))

    def loop(self, animation):
        self._layer.set_animation('%s.%s' % (self._resource_id, animation))
