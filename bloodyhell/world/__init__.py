from bloodyhell.world.camera import Camera

from bloodyhell.box2d.collision.b2aabb import b2AABB
from bloodyhell.box2d.dynamics.b2world import b2World
from bloodyhell.box2d.common.math.b2vec2 import b2Vec2


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
        worldAABB.minVertex.Set(-1000, -1000)
        worldAABB.maxVertex.Set(1000, 1000)
        gravity_x, gravity_y = gravity
        gravity = b2Vec2(gravity_x, gravity_y)
        self._box2d_world = b2World(worldAABB, gravity, True)

    def add(self, chunk, slot):
        chunk.set_camera(self._camera)
        chunk.append_to_world(self._box2d_world)
        self._chunks.append(chunk)
        self._root_layer.addLayer(chunk.layer(), slot)
        self._root_layer.add(chunk)

    def step(self, delta):
        self._box2d_world.Step(delta, 1)
        self._camera.update()
        for chunk in self._chunks:
            chunk.update()

    def camera(self):
        return self._camera
