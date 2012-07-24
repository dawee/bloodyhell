from bloodyhell.world.chunk import Chunk

from bloodyhell.box2d.collision.shapes.b2boxdef import b2BoxDef
from bloodyhell.box2d.dynamics.b2bodydef import b2BodyDef


class Fence(Chunk):

    def __init__(self, position, size,
                        resource_id=None, default_animation=None):
        super(Fence, self).__init__(position, size)
        if resource_id is not None:
            self._resource_id = resource_id
            self.loop(default_animation)

    def append_to_world(self, world):
        width, height = self._size
        x, y = self._position
        box_def = b2BoxDef()
        box_def.extents.Set(width, height)
        body_def = b2BodyDef()
        body_def.AddShape(box_def)
        body_def.position.Set(x, y)
        self._body = world.CreateBody(body_def)

    def loop(self, animation):
        self._layer.set_animation('%s.%s' % (self._resource_id, animation))
