from bloodyhell.layer.animatedlayer import AnimatedLayer
from bloodyhell.eventdispatcher import EventDispatcher


class Chunk(EventDispatcher):

    def __init__(self, position, size):
        super(Chunk, self).__init__()
        self._camera = None
        self._layer = AnimatedLayer()
        self._position = position
        self._size = size
        self._body = None
        self._geometry = None
        self._pasted = True

    def pasted(self):
        return self._pasted

    def paste(self, value):
        self._pasted = value

    def append_to_world(self, world, space):
        pass

    def set_camera(self, camera):
        self._camera = camera

    def update(self):
        if self._geometry is not None:
            x, y, z = self._geometry.getPosition()
            self._position = (x, y)
        if self._camera:
            self._camera.set_layer_rect(
                self._layer, self._position, self._size
            )

    def layer(self):
        return self._layer

    def set_position(self, position):
        self._position = position
        if self._geometry is not None:
            x, y = position
            self._geometry.setPosition((x, y, -0.5))

    def on_collision(self, world, chunk, contacts, contact_group):
        return False

    def fill(self, color):
        self._layer.fill(color)

    def position(self):
        return self._position

    def size(self):
        return self._size

    def body(self):
        return self._body

    def set_x_velocity(self, new_x_velocity):
        if self._body:
            x_vel, y_vel, z_vel = self._body.getLinearVel()
            self._body.setLinearVel((new_x_velocity, y_vel, z_vel))

    def set_y_velocity(self, new_y_velocity):
        if self._body:
            x_vel, y_vel, z_vel = self._body.getLinearVel()
            self._body.setLinearVel((x_vel, new_y_velocity, z_vel))
            if new_y_velocity > 0:
                self.paste(False)
