import os
import sys

sys.path.append(os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', '..', 'src')
))

from bloodyhell.game import Game
from bloodyhell.level import Level
from bloodyhell.layer.animatedlayer import AnimatedLayer
from bloodyhell.layer.rect import Rect
from bloodyhell.world.actor import Actor
from bloodyhell.world.decoration import Decoration

RESOLUTION = (200, 150)


class FirstLevel(Level):

    def __init__(self):
        super(FirstLevel, self).__init__(camera_config={
            'target': (20, 20),
            'width': 40,
            'rect': Rect((0, 0), RESOLUTION),
            'limits': {'left': 0, 'bottom': 0,
                       'right': 200, 'top': 50}
        }, gravity=(0, -1, 0))
        self.loader().load_package('sprites')
        self.loader().load_package('sample')
        self.listen('quit')
        background = Decoration((0, 50), (200, 50))
        background._layer.set_image('sample.backgrounds.bg1')
        self.add_chunk(background, self.BACKGROUND)
        aladdin = Actor(
            'sprites.walker',
            'walk',
            position=(5, 20),
            size=(0.5, 1.8)
        )
        self.add_chunk(aladdin, self.SPRITES)
        self.listen_key('down')

    def on_down_pressed(self):
        target_x, target_y = self.world().camera().target()
        self.world().camera().set_target((target_x, target_y - 1))

    def on_down_released(self):
        print 'right released'

    def on_quit(self, event):
        sys.exit()


def run():
    resources_folder = os.path.join(os.path.dirname(__file__), 'res')
    game = Game('Sample', RESOLUTION, resources_folder)
    game.navigator().set_current_view(FirstLevel())
    game.run()


if __name__ == '__main__':
    run()
