from bloodyhell.world.chunk import Chunk

from Box2D import b2PolygonDef
from Box2D import b2BodyDef


class Fence(Chunk):

    FIXED_BORDER = 0.02

    def __init__(self, position, size,
                        resource_id=None, default_animation=None):
        super(Fence, self).__init__(position, size)
        if resource_id is not None:
            if default_animation is not None:
                self._resource_id = resource_id
                self.loop(default_animation)
            else:
                self._layer.set_image(resource_id)

    def append_to_world(self, world):
        width, height = self._size
        x, y = self._position
        box = b2PolygonDef()
        hitbox_width = (self._hitbox.left * width / 100) * 2
        hitbox_height = (self._hitbox.top * height / 100) * 2
        box.SetAsBox((width / 2) - hitbox_width, (height / 2) - hitbox_height)
        body_def = b2BodyDef()
        body_def.position.Set(x, y)
        self._body = world.CreateBody(body_def)
        self._body.CreateShape(box)

    def loop(self, animation):
        self._layer.set_animation('%s.%s' % (self._resource_id, animation))
