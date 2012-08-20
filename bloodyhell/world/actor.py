from bloodyhell.world.chunk import Chunk


from Box2D import b2PolygonDef
from Box2D import b2BodyDef


class Actor(Chunk):

    HUMAN_DENSITY = 1010

    def __init__(self, resource_id, default_animation,
                         position, size, density=HUMAN_DENSITY):
        super(Actor, self).__init__(position, size)
        self._resource_id = resource_id
        self.loop(default_animation)
        self._density = density

    def append_to_world(self, world):
        self.world = world
        width, height = self._size
        x, y = self._position
        box = b2PolygonDef()
        box.SetAsBox(width / 2, height / 2)
        box.density = self._density
        box.friction = 0
        box.angle = 0
        box.restitution = 0
        body_def = b2BodyDef()
        body_def.fixedRotation = True
        body_def.position.Set(x, y)
        self._body = world.CreateBody(body_def)
        self._body.CreateShape(box)
        self._body.SetMassFromShapes()

    def loop(self, animation):
        self._layer.set_animation('%s.%s' % (self._resource_id, animation))
