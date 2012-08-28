from bloodyhell.world.camera import Camera

from Box2D import b2AABB
from Box2D import b2World
from Box2D import b2Vec2
from Box2D import b2ContactListener


class ContactListener(b2ContactListener):

    def Add(self, point):
        chunk1 = point.shape1.GetBody().userData
        chunk2 = point.shape2.GetBody().userData
        if hasattr(chunk1, 'on_collision') and hasattr(chunk2, 'on_collision'):
            if not chunk1.on_collision(chunk2, point):
                chunk2.on_collision(chunk1, point)


class World(object):

    def __init__(self, root_layer, camera_config, gravity=(0, 0, 0)):
        self._camera = Camera(
            target=camera_config['target'],
            width=camera_config['width'],
            rect=camera_config['rect'],
            limits=camera_config['limits'],
        )
        self._root_layer = root_layer
        self._chunks = []
        worldAABB = b2AABB()
        worldAABB.lowerBound = (-1000, -1000)
        worldAABB.upperBound = (1000, 1000)
        gravity_x, gravity_y = gravity
        gravity = b2Vec2(gravity_x, gravity_y)
        self._box2d_world = b2World(worldAABB, gravity, True)
        self._contact_listener = ContactListener()
        self._box2d_world.SetContactListener(self._contact_listener)
        self._remove_list = []

    def _remove(self, chunk):
        if chunk._body:
            chunk._body.userData = None
            self._box2d_world.DestroyBody(chunk._body)
            chunk._body = None

    def remove(self, chunk):
        self._remove_list.append(chunk)
        self._root_layer.remove(chunk)
        self._root_layer.remove_layer(chunk.layer())

    def add(self, chunk, slot):
        chunk.set_camera(self._camera)
        chunk.append_to_world(self._box2d_world)
        chunk.set_user_data()
        self._chunks.append(chunk)
        self._root_layer.add_layer(chunk.layer(), slot)
        self._root_layer.add(chunk)

    def step(self, delta):
        for chunk in self._remove_list:
            self._remove(chunk)
        self._remove_list = []
        self._box2d_world.Step(delta, 8, 1)
        self._camera.update()
        for chunk in self._chunks:
            chunk.update()

    def camera(self):
        return self._camera
