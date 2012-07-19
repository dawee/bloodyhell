import ode
from bloodyhell.world.chunk import Chunk


class Fence(Chunk):

    def __init__(self, position, size,
                        resource_id=None, default_animation=None):
        super(Fence, self).__init__(position, size)
        if resource_id is not None:
            self._resource_id = resource_id
            self.loop(default_animation)

    def append_to_world(self, world, space):
        width, height = self._size
        self._geometry = ode.GeomBox(space, lengths=(width, height, 1))
        x, y = self._position
        self._geometry.setPosition((x, y, -0.5))
        self._geometry.chunk = self

    def loop(self, animation):
        self._layer.set_animation('%s.%s' % (self._resource_id, animation))

    def on_collision(self, world, chunk, contacts, contact_group):
        chunk_x, chunk_y = chunk.position()
        x, y = self.position()
        if chunk_y > y:
            if chunk.pasted():
                slider_joint = ode.SliderJoint(world, contact_group)
                slider_joint.setAxis((1, 0, 0))
                slider_joint.attach(chunk.body(), self.body())
                chunk.set_y_velocity(0)
                return True
            else:
                chunk.paste(True)
        else:
            for contact in contacts:
                contact_joint = ode.ContactJoint(world, contact_group, contact)
                contact_joint.attach(chunk.body(), self.body())
