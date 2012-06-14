import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'src')))

from bloodyhell.game import Game
from bloodyhell.view import View
from bloodyhell.layer import Layer


class SquareActor(Layer):

    def __init__(self, *args, **kwargs):
        super(SquareActor, self).__init__(*args, **kwargs)
        self.listen_key('right')

    def on_right_pressed(self):
        print 'right pressed'

    def on_right_released(self):
        print 'right released'


class PrintRight(View):

    def __init__(self, *args, **kwargs):
        super(PrintRight, self).__init__(*args, **kwargs)
        self.load_package('sprites')
        self.fill((0, 0, 0))
        layer = self.addLayer((100, 100), (300, 300))
        layer.fill((0, 0, 0))
        actor = layer.addLayer((10, 10), (30, 30), SquareActor)
        from bloodyhell.resourceloader import ResourceLoader
        print ResourceLoader().get_animation_frames('sprites.walker.walk')
        self.listen('quit')

    def on_quit(self, event):
        sys.exit()

def run():
    game = Game(
        'Sample',
        (800, 600),
        os.path.join(os.path.dirname(__file__), 'res'),
        PrintRight
    )
    game.run()

if __name__ == '__main__':
    run()