from bloodyhell.layer.rect import Rect


class Camera(object):

    def __init__(self, target, width, rect, limits):
        self._rect = rect
        self._target = target
        self._width = width
        self._height = (self._width * self._rect.height) / self._rect.width
        self._limits = limits
        self._actor_to_watch = None
        self._actor_top_offset = 0
        self._actor_left_offset = 0
        self._y_high_filter_threshold = 1.0
        self._width_low_filter = 0.2
        self._required_width = width

    def set_y_high_filter_threshold(self, threshold):
        self._y_high_filter_threshold = threshold

    def update_width(self):
        old_width = self._width
        value_diff = self._required_width - old_width
        value_diff *= self._width_low_filter
        self._width = old_width + value_diff
        self._height = (self._width * self._rect.height) / self._rect.width

    def set_width(self, width):
        self._required_width = width

    def set_layer_rect(self, layer, world_position, world_size):
        world_width, world_height = world_size
        world_x, world_y = world_position
        layer.rect().width = (self._rect.width * world_width) / self._width
        layer.rect().height = (self._rect.height * world_height) / self._height
        centered_x, centered_y = self._get_layer_point(world_position)
        layer.rect().x = centered_x - layer.rect().width / 2
        layer.rect().y = centered_y - layer.rect().height / 2

        if layer.rect().right <= self._rect.x \
                or self._rect.right <= layer.rect().x \
                or layer.rect().bottom <= self._rect.y \
                or self._rect.bottom <= layer.rect().y:
            # Layer is not visible
            layer.set_cropped_rect(None)
        else:
            cropped_rect = Rect(
                0, 0, layer.rect().width, layer.rect().height
            )
            if layer.rect().x < self._rect.x:
                cropped_rect.x = self._rect.x - layer.rect().x
                cropped_rect.width -= cropped_rect.x
            if layer.rect().right > self._rect.right:
                cropped_rect.width -= (layer.rect().right - self._rect.right)
            if layer.rect().y < self._rect.y:
                cropped_rect.y = self._rect.y - layer.rect().y
                cropped_rect.height -= cropped_rect.y
            if layer.rect().bottom > self._rect.bottom:
                cropped_rect.height -= (layer.rect().bottom - self._rect.bottom)
            layer.set_cropped_rect(cropped_rect)

    def _get_layer_point(self, world_point):
        world_point_x, world_point_y = world_point
        target_world_x, target_world_y = self._target
        target_graph_x, target_graph_y = (
            self._rect.width / 2,
            self._rect.height / 2
        )
        world_x_offset, world_y_offset = (
            world_point_x - target_world_x,
            world_point_y - target_world_y,
        )
        graph_x_offset, graph_y_offset = (
            world_x_offset * self._rect.width / self._width,
            -world_y_offset * self._rect.height / self._height,
        )
        return (
            target_graph_x + graph_x_offset,
            target_graph_y + graph_y_offset
        )

    def set_target(self, target):
        target_x, target_y = target
        old_x, old_y = self._target
        value_diff = target_y - old_y
        if value_diff == 0:
            high_filter = 1.0
        else:
            high_filter = abs(value_diff) / self._y_high_filter_threshold
        value_diff *= high_filter
        if abs(value_diff * high_filter) < abs(value_diff):
            target_y = old_y + value_diff
        self._target = (target_x, target_y)

    def target(self):
        return self._target

    def watch(self, actor, top_offset=0, left_offset=0):
        self._actor_to_watch = actor
        self._actor_top_offset = top_offset
        self._actor_left_offset = left_offset

    def update(self):
        if self._actor_to_watch is not None:
            actor_x, actor_y = self._actor_to_watch.position()
            actor_width, actor_height = self._actor_to_watch.size()
            target_y = actor_y + self._actor_left_offset
            self.set_target((
                actor_x + self._actor_left_offset,
                target_y,
            ))
        self.update_width()
