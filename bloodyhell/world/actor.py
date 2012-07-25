from bloodyhell.world.chunk import Chunk

from bloodyhell.box2d.collision.shapes.b2boxdef import b2BoxDef
from bloodyhell.box2d.dynamics.b2bodydef import b2BodyDef


class Actor(Chunk):

    HUMAN_DENSITY = 1010

    def __init__(self, resource_id, default_animation,
                         position, size, density=HUMAN_DENSITY):
        super(Actor, self).__init__(position, size)
        self._resource_id = resource_id
        self.loop(default_animation)
        self._density = density

    def update(self):
        super(Actor, self).update()

    def append_to_world(self, world):
        width, height = self._size
        x, y = self._position
        box_def = b2BoxDef()
        box_def.friction = 0
        box_def.restitution = 1.0
        box_def.density = self._density
        box_def.extents.Set(width, height)
        body_def = b2BodyDef()
        body_def.AddShape(box_def)
        body_def.position.Set(x, y)
        self._body = world.CreateBody(body_def)

    def loop(self, animation):
        self._layer.set_animation('%s.%s' % (self._resource_id, animation))
