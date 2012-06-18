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
from bloodyhell.world.stence import Stence

import ode

RESOLUTION = (800, 600)

class Aladdin(Actor):

    def __init__(self, position, size):
        super(Aladdin, self).__init__(
            'sprites.walker', 'walk', position, size
        )

class FirstLevel(Level):

    def __init__(self):
        super(FirstLevel, self).__init__(camera_config={
            'target': (5, 3.5),
            'width': 10,
            'rect': Rect((0, 0), RESOLUTION),
            'limits': {'left': 0, 'bottom': 0,
                       'right': 70, 'top': 10}
        }, gravity=(0, -9.8, 0))
        self.listen('quit')
        # Load resources
        self.loader().load_package('sprites')
        self.loader().load_package('sample')
        # Create Background
        background = Decoration((0, 10), (70, 10))
        background._layer.set_image('sample.backgrounds.bg1')
        self.add_chunk(background, self.BACKGROUND)
        # Create Actor (aladdin)
        aladdin = Aladdin(position=(0.5, 10), size=(1, 1.7))
        self.add_chunk(aladdin, self.SPRITES)
        # Create Ground
        ground = Stence((0, 0.8), (70, 1))
        self.add_chunk(ground, self.FAR_DECORATION)

    def on_quit(self, event):
        sys.exit()


def run():
    resources_folder = os.path.join(os.path.dirname(__file__), 'res')
    game = Game('Sample', RESOLUTION, resources_folder, fps=25)
    game.navigator().set_current_view(FirstLevel())
    game.run()


if __name__ == '__main__':
    run()
