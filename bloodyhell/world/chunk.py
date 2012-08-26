from bloodyhell.layer.animatedlayer import AnimatedLayer
from bloodyhell.eventdispatcher import EventDispatcher
from bloodyhell.layer.rect import Rect


class Chunk(EventDispatcher):

    def __init__(self, position, size):
        super(Chunk, self).__init__()
        self._camera = None
        self._layer = AnimatedLayer()
        self._position = position
        self._size = size
        self._body = None
        self._pasted = True
        self._hitbox = Rect(0, 0, 0, 0)

    def set_hitbox(self, hitbox):
        self._hitbox.left = hitbox.get('left', self._hitbox.left)
        self._hitbox.top = hitbox.get('top', self._hitbox.top)
        self._hitbox.bottom = hitbox.get('bottom', self._hitbox.bottom)
        self._hitbox.right = hitbox.get('right', self._hitbox.right)

    def pasted(self):
        return self._pasted

    def paste(self, value):
        self._pasted = value

    def append_to_world(self, world):
        pass

    def set_user_data(self):
        if self._body is not None:
            self._body.userData = self

    def set_camera(self, camera):
        self._camera = camera

    def on_collision(self, chunk, point):
        pass

    def update(self):
        if self._body is not None:
            self._position = (
                self._body.GetPosition().x,
                self._body.GetPosition().y
            )
        if self._camera:
            self._camera.set_layer_rect(
                self._layer, self._position, self._size
            )

    def layer(self):
        return self._layer

    def set_position(self, position):
        self._position = position
        if self._body is not None:
            x, y = position
            self._body.SetCenterPosition(x, y)

    def fill(self, color):
        self._layer.fill(color)

    def position(self):
        return self._position

    def size(self):
        return self._size

    def hitbox(self):
        return self._hitbox

    def body(self):
        return self._body

    def set_x_velocity(self, new_x_velocity):
        if self._body:
            self._body.WakeUp()
            velocity = self._body.GetLinearVelocity()
            velocity.x = new_x_velocity
            self._body.SetLinearVelocity(velocity)

    def set_y_velocity(self, new_y_velocity):
        if self._body:
            self._body.WakeUp()
            velocity = self._body.GetLinearVelocity()
            velocity.y = new_y_velocity
            self._body.SetLinearVelocity(velocity)
            if new_y_velocity > 0:
                self.paste(False)

    def get_y_velocity(self):
        return self._body.GetLinearVelocity().y

    def contains(self, chunk):
        chunk_x, chunk_y = chunk.position()
        chunk_width, chunk_height = chunk.size()
        self_x, self_y = self._position
        self_width, self_height = self._size

        self_x += (self._hitbox.left * self_width) / 100
        self_y += (self._hitbox.top * self_height) / 100
        self_width -= 2 * self_x
        self_height -= 2 * self_y

        chunk_x += (chunk.hitbox().left * chunk_width) / 100
        chunk_y += (chunk.hitbox().top * chunk_height) / 100
        chunk_width -= 2 * chunk_x
        chunk_height -= 2 * chunk_y

        if chunk_x >= self_x and chunk_x <= self_x + self_width / 2 \
            and chunk_y >= self_y and chunk_y <= self_y + self_height / 2:
                return True
        else:
            return False
