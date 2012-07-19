import ode
from bloodyhell.world.chunk import Chunk


class Actor(Chunk):

    HUMAN_DENSITY = 1010

    def __init__(self, resource_id, default_animation,
                         position, size, density=HUMAN_DENSITY):
        super(Actor, self).__init__(position, size)
        self._resource_id = resource_id
        self.loop(default_animation)
        self._density = density

    def append_to_world(self, world, space):
        width, height = self._size
        self._body = ode.Body(world)
        mass = ode.Mass()
        mass.setBox(self._density, width, height, width)
        self._body.setMass(mass)
        self._geometry = ode.GeomBox(space, lengths=(width, height, 1))
        self._geometry.setBody(self._body)
        x, y = self._position
        self._geometry.setPosition((x, y, -0.5))
        self._geometry.chunk = self

    def loop(self, animation):
        self._layer.set_animation('%s.%s' % (self._resource_id, animation))
