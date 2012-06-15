from bloodyhell.world import World
from bloodyhell.view import View


class Level(View):

    (
        # Background slots
        BACKGROUND, BACKGROUND_1, BACKGROUND_2,
        # Platform slots
        PLATFORM, PLATFORM_1, PLATFORM_2,
        # Far decoration slots (sprites are in front of this)
        FAR_DECORATION, FAR_DECORATION_1, FAR_DECORATION_2,
        # Sprites slots (actors, monsters, objects)
        SPRITES, SPRITES_1, SPRITES_2,
        # Near decoration slots (sprites are behind this)
        NEAR_DECORATION, NEAR_DECORATION_1, NEAR_DECORATION_2,
    ) = range(15)

    def __init__(self, camera_config, gravity):
        super(Level, self).__init__()
        self._world = World(self, camera_config, gravity)

    def add_chunk(self, chunk, slot):
        self._world.add(chunk, slot)

    def on_frame(self, delta):
        self._world.step(delta)
        super(Level, self).on_frame(delta)

    def world(self):
        return self._world
