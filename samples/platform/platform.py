import os
import sys

sys.path.append(os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', '..')
))

from bloodyhell.game import Game
from bloodyhell.level import Level
from bloodyhell.layer.rect import Rect
from bloodyhell.layer import Layer
from bloodyhell.world.actor import Actor
from bloodyhell.world.decoration import Decoration
from bloodyhell.world.fence import Fence


RESOLUTION = (800, 600)
FPS = 25


class Mario(Actor):

    def __init__(self, position, size):
        super(Mario, self).__init__(
            'platform.sprites.mario', 'stance', position, size
        )
        self.listen_key('right')
        self.listen_key('up')
        self._walking = False

    def update(self):
        super(Mario, self).update()
        if self._walking:
            self.set_x_velocity(6.0)

    def on_right_pressed(self):
        self._walking = True
        #self.loop('walk')

    def on_right_released(self):
        self._walking = False
        self.set_x_velocity(0.0)
        #self.loop('stance')

    def on_up_pressed(self):
        self.set_y_velocity(6.0)

    def on_up_released(self):
        pass


class FirstLevel(Level):

    def __init__(self):
        res_width, res_height = RESOLUTION
        super(FirstLevel, self).__init__(camera_config={
            'target': (5.0, 3.5),
            'width': 15.0,
            'rect': Rect((10, 10), (res_width - 20, res_height - 20)),
            'limits': {'left': 0.0, 'bottom': 0.0,
                       'right': 70.0, 'top': 10.0}
        }, gravity=(0, -9.8))
        self.listen('quit')
        # Load resources
        self.loader().load_package('platform')
        # Add background (filled with skyblue)
        self.add_layer(
            Layer(position=(0, 0), size=RESOLUTION).fill('87CEEB'),
            self.BACKGROUND
        )
        for i in range(10):
            for j in range(10):
                self.add_chunk(
                    Fence(
                        (0.25 + j + i * 0.49, 2.0 + j),
                        (0.5, 0.5),
                        'platform.static.brick'
                    ),
                    self.PLATFORM
                )

        # Create Actor (mario)
        mario = Mario(position=(2.0, 4.0), size=(0.5, 1.0))
        self.add_chunk(mario, self.SPRITES)

        # Lock camera to Mario
        self.world().camera().watch(mario)

    def on_quit(self, event):
        sys.exit()


def run():
    game = Game(
        'BloodyHell Sample : Platform game',
        RESOLUTION,
        os.path.join(os.path.dirname(__file__), 'res'),
        fps=FPS
    )
    game.navigator().set_current_view(FirstLevel())
    game.run()


if __name__ == '__main__':
    run()
