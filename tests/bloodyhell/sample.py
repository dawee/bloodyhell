import os
import sys

sys.path.append(os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', '..', 'src')
))

from bloodyhell.game import Game
from bloodyhell.level import Level
from bloodyhell.layer.rect import Rect
from bloodyhell.world.actor import Actor
from bloodyhell.world.decoration import Decoration
from bloodyhell.world.fence import Fence


RESOLUTION = (1024, 768)


class Aladdin(Actor):

    def __init__(self, position, size):
        super(Aladdin, self).__init__(
            'sprites.aladdin', 'stance', position, size
        )
        self.listen_key('right')
        self.listen_key('up')

    def on_right_pressed(self):
        self.set_x_velocity(10)
        self.loop('walk')

    def on_right_released(self):
        self.set_x_velocity(0)
        self.loop('stance')

    def on_up_pressed(self):
        self.set_y_velocity(10)

    def on_up_released(self):
        pass


class FirstLevel(Level):

    def __init__(self):
        res_width, res_height = RESOLUTION
        super(FirstLevel, self).__init__(camera_config={
            'target': (5.0, 3.5),
            'width': 10.0,
            'rect': Rect((10, 10), (res_width - 20, res_height - 200)),
            'limits': {'left': 0.0, 'bottom': 0.0,
                       'right': 70.0, 'top': 10.0}
        }, gravity=(0, -9.8, 0))
        self.listen('quit')
        # Load resources
        self.loader().load_package('sprites')
        self.loader().load_package('sample')
        # Create Background
        self.add_chunk(
            Decoration((35.0, 5.0), (70.0, 10.0), 'sample.backgrounds.bg1'),
            self.BACKGROUND
        )
        # Create Actor (aladdin)
        aladdin = Aladdin(position=(0.5, 10.0), size=(1.0, 1.7))
        self.add_chunk(aladdin, self.SPRITES)
        # Create Ground
        self.add_chunk(Fence((35.0, 0), (70.0, 1)), self.PLATFORM)
        # Lock camera to Aladdin
        self.world().camera().watch(aladdin)

    def on_quit(self, event):
        sys.exit()


def run():
    resources_folder = os.path.join(os.path.dirname(__file__), 'res')
    game = Game('Sample', RESOLUTION, resources_folder, fps=25)
    game.navigator().set_current_view(FirstLevel())
    game.run()


if __name__ == '__main__':
    run()
