import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'src')))

from bloodyhell.game import Game
from bloodyhell.level import Level
from bloodyhell.layer.animatedlayer import AnimatedLayer
from bloodyhell.layer.rect import Rect
from bloodyhell.world.chunk import Chunk

RESOLUTION = (800, 600)

class Aladdin(AnimatedLayer):

    def __init__(self):
        super(Aladdin, self).__init__()
        self.listen_key('right')

    def on_right_pressed(self):
        print 'right pressed'

    def on_right_released(self):
        print 'right released'


class FirstLevel(Level):

    def __init__(self):
        super(FirstLevel, self).__init__(camera_config={
            'target': (20, 20),
            'width': 40,
            'rect': Rect((0, 0), RESOLUTION),
            'limits': {'left': 0, 'bottom': 0,
                       'right': 200, 'top': 50}
        })
        self.load_package('sprites')
        self.load_package('sample')
        self.listen('quit')
        background = Chunk((0, 50), (200, 50))
        background._layer.set_image('sample.backgrounds.bg1')
        self.add_chunk(background, self.BACKGROUND)
        self.listen_key('down')

    def on_down_pressed(self):
        target_x, target_y = self.world().camera().target()
        self.world().camera().set_target((target_x, target_y - 1))

    def on_down_released(self):
        print 'right released'

    def on_quit(self, event):
        sys.exit()


def run():
    resources_folder =  os.path.join(os.path.dirname(__file__), 'res')
    game = Game('Sample', RESOLUTION, resources_folder)
    game.navigator().set_current_view(FirstLevel())
    game.run()


if __name__ == '__main__':
    run()
