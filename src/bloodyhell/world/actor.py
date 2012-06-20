import ode
from bloodyhell.world.chunk import Chunk
from bloodyhell.world.fence import Fence


class Actor(Chunk):

    HUMAN_DENSITY = 1010

    def __init__(self, resource_id, default_animation,
                         position, size, density=HUMAN_DENSITY):
        super(Actor, self).__init__(position, size)
        self._resource_id = resource_id
        self.loop(default_animation)
        self._density = density
        self._paste = True

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

    def set_x_velocity(self, new_x_velocity):
        x_vel, y_vel, z_vel = self._body.getLinearVel()
        self._body.setLinearVel((new_x_velocity, y_vel, z_vel))

    def set_y_velocity(self, new_y_velocity):
        x_vel, y_vel, z_vel = self._body.getLinearVel()
        self._body.setLinearVel((x_vel, new_y_velocity, z_vel))
        if new_y_velocity > 0:
            self._paste = False

    def loop(self, animation):
        self._layer.set_animation('%s.%s' % (self._resource_id, animation))

    def on_collision(self, world, chunk, contacts, contact_group):
        if isinstance(chunk, Fence) and self._paste:
            chunk_x, chunk_y = chunk.position()
            x, y = self.position()
            width, height = self.size()
            if y + height >= chunk_y:
                slider_joint = ode.SliderJoint(world, contact_group)
                slider_joint.setAxis((1, 0, 0))
                slider_joint.attach(self.body(), chunk.body())
                return True
        self._paste = True
