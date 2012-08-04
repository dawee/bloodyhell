import os
import sys

if not hasattr(sys, 'frozen'):
    APP_DIR = os.path.dirname(__file__)
else:
    APP_DIR = os.path.dirname(os.path.abspath(sys.executable))

sys.path.append(os.path.abspath(
    os.path.join(APP_DIR, '..', '..')
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

    (LEFT, RIGHT) = range(3)[1:]

    def __init__(self, position, size):
        super(Mario, self).__init__(
            'platform.sprites.mario', 'stance', position, size
        )
        self.listen_key('right')
        self.listen_key('left')
        self.listen_key('up')
        self._walking = None

    def update(self):
        super(Mario, self).update()
        if self._walking == self.RIGHT:
            self.set_x_velocity(6.0)
        elif self._walking == self.LEFT:
            self.set_x_velocity(-6.0)

    def on_right_pressed(self):
        self._walking = self.RIGHT
        #self.loop('walk')

    def on_right_released(self):
        self._walking = None
        self.set_x_velocity(0.0)
        #self.loop('stance')

    def on_left_pressed(self):
        self._walking = self.LEFT
        #self.loop('walk')

    def on_left_released(self):
        self._walking = None
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

        # Create Actor (mario)
        mario = Mario(position=(1.5, 4.0), size=(0.5, 1.0))
        self.add_chunk(mario, self.SPRITES)

        # Lock camera to Mario
        self.world().camera().watch(mario)

        from Box2D import *
        body_def = b2BodyDef()
        body_def.position.Set(0, 0)
        body = mario.world.CreateBody(body_def)
        for j in range(10):
            for i in range(10):
                self.add_chunk(
                    Fence(
                        (0.25 + j * 2 + i * 0.5, 2.0 + j * 3),
                        (0.5, 0.5),
                        'platform.static.brick'
                    ),
                    self.PLATFORM
                )
            edgeDef = b2EdgeChainDef()
            edgeDef.vertices = [
                (0.25 + j * 5, 2.75 + j * 3),
                (0.25 + j * 5 + 5, 2.75 + j * 3)
            ]
            body.CreateShape(edgeDef)


    def on_quit(self, event):
        sys.exit()


def run():
    game = Game(
        'BloodyHell Sample : Platform game',
        RESOLUTION,
        os.path.join(APP_DIR, 'res'),
        fps=FPS
    )
    game.navigator().set_current_view(FirstLevel())
    game.run()


if __name__ == '__main__':
    run()
