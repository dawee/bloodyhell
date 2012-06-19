

class Camera(object):

    def __init__(self, target, width, rect, limits):
        self._rect = rect
        self._target = target
        self._width = width
        self._height = (self._width * self._rect.height) / self._rect.width
        self._limits = limits
        self._actor_to_watch = None

    def set_layer_rect(self, layer, world_position, world_size):
        world_width, world_height = world_size
        layer.rect().width = (self._rect.width * world_width) / self._width
        layer.rect().height = (self._rect.height * world_height) / self._height
        centered_x, centered_y = self._get_layer_point(world_position)
        layer.rect().x = centered_x - layer.rect().width / 2
        layer.rect().y = centered_y - layer.rect().height / 2

    def _get_layer_point(self, world_point):
        target_x, target_y = self._target
        if target_x - self._width / 2 < self._limits['left']:
            target_x = self._limits['left'] + self._width / 2
        if target_x + self._width / 2 > self._limits['right']:
            target_x = self._limits['right'] - self._width / 2
        if target_y - self._height / 2 < self._limits['bottom']:
            target_y = self._limits['bottom'] + self._height / 2
        if target_y + self._height / 2 > self._limits['top']:
            target_y = self._limits['top'] - self._height / 2
        world_x, world_y = world_point
        target_layer_x, target_layer_y = (
            self._rect.x + (self._rect.width / 2),
            self._rect.y + (self._rect.height / 2)
        )
        layer_offset_x, layer_offset_y = (
            (world_x - target_x) * self._rect.width / self._width,
            (world_y - target_y) * self._rect.height / self._height
        )
        return (
            target_layer_x + layer_offset_x,
            target_layer_y - layer_offset_y,
        )

    def set_target(self, target):
        self._target = target

    def target(self):
        return self._target

    def watch(self, actor):
        self._actor_to_watch = actor

    def update(self):
        if self._actor_to_watch is not None:
            actor_x, actor_y = self._actor_to_watch.position()
            actor_width, actor_height = self._actor_to_watch.size()
            self.set_target((
                actor_x + (actor_width / 2),
                actor_y + (actor_height / 2),
            ))
