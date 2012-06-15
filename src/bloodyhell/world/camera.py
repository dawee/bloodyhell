

class Camera(object):

    def __init__(self, target, width, rect, limits):
        self._rect = rect
        self._target = target
        self._width = width
        self._height = (self._width * self._rect.height) / self._rect.width
        self._limits = limits

    def set_layer_rect(self, layer, world_position, world_size):
        world_width, world_height = world_size
        layer.rect().width = (self._rect.width * world_width) / self._width
        layer.rect().height = (self._rect.height * world_height) / self._height
        layer.rect().x, layer.rect().y = self._get_layer_point(world_position)

    def _get_layer_point(self, world_point):
        target_x, target_y = self._target
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
