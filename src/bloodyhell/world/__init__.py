import ode
from bloodyhell.world.camera import Camera


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
        self._ode_world = ode.World()
        self._ode_world.setGravity(gravity)
        self._space = ode.Space()

    def add(self, chunk, slot):
        chunk.set_camera(self._camera)
        chunk.append_to_world(self._ode_world, self._space)
        self._chunks.append(chunk)
        self._root_layer.addLayer(chunk.layer(), slot)

    def step(self, delta):
        self._ode_world.step(delta)
        for chunk in self._chunks:
            chunk.update_rect()

    def camera(self):
        return self._camera
