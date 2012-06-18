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
        self._contact_group = ode.JointGroup()

    def add(self, chunk, slot):
        chunk.set_camera(self._camera)
        chunk.append_to_world(self._ode_world, self._space)
        self._chunks.append(chunk)
        self._root_layer.addLayer(chunk.layer(), slot)

    def step(self, delta):
        self._space.collide(
            (self._ode_world, self._contact_group),
            self._near_callback
        )
        self._ode_world.step(delta)
        for chunk in self._chunks:
            chunk.set_pending_position()
            chunk.update_rect()
        self._contact_group.empty()

    def camera(self):
        return self._camera

    def _near_callback(self, args, geom1, geom2):
        chunk1 = geom1.chunk
        chunk2 = geom2.chunk
        contacts = ode.collide(geom1, geom2)
        world, contact_group = args
        if not chunk1.on_collision(world, chunk2, contacts, contact_group):
            chunk2.on_collision(world, chunk1, contacts, contact_group)