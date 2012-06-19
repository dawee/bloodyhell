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
        self._x_linear_velocity = 0
        self._y_linear_velocity = 0
        self._contact_group = ode.JointGroup()

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

    def loop(self, animation):
        self._layer.set_animation('%s.%s' % (self._resource_id, animation))

    def set_linear_velocity(self, velocity):
        self._contact_group.empty()
        self._x_linear_velocity, self._y_linear_velocity = velocity
        self._body.setLinearVel(
            (self._x_linear_velocity, self._y_linear_velocity, 0)
        )

    def _is_going_in_opposite_way(self, chunk):
        chunk_x, chunk_y = chunk.position()
        chunk_width, chunk_height = chunk.position()
        x, y = self.position()
        width, height = self.size()
        if x + width <= chunk_x and self._x_linear_velocity < 0 \
                or chunk_x + chunk_width <= x and self._x_linear_velocity > 0 \
                or y + height <= chunk_y and self._y_linear_velocity > 0 \
                or chunk_y + chunk_height <= y and self._y_linear_velocity < 0:
            return True
        else:
            return False

    def on_collision(self, world, chunk, contacts, contact_group):
        self._contact_group.empty()
        """
        if self._is_going_in_opposite_way(chunk):
            return False
        """
        if isinstance(chunk, Fence):
            chunk_x, chunk_y = chunk.position()
            x, y = self.position()
            width, height = self.size()
            if y + height >= chunk_y:
                slider_joint = ode.SliderJoint(world, self._contact_group)
                slider_joint.setAxis((1, 0, 0))
                slider_joint.attach(self.body(), chunk.body())
                return True
