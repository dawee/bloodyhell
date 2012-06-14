import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'src')))

from bloodyhell.game import Game
from bloodyhell.view import View
from bloodyhell.animatedlayer import AnimatedLayer


class Aladdin(AnimatedLayer):

    def __init__(self):
        super(Aladdin, self).__init__()
        self.listen_key('right')

    def on_right_pressed(self):
        print 'right pressed'

    def on_right_released(self):
        print 'right released'


class FirstLevel(View):

    def __init__(self):
        super(FirstLevel, self).__init__()
        self.load_package('sprites')
        self.load_package('sample')
        self.set_image('sample.backgrounds.bg1')
        aladdin = Aladdin()
        self.addLayer(aladdin)
        aladdin.set_animation('sprites.walker.walk')
        aladdin.rect().y = self.rect().height - aladdin.rect().height - 30
        self.listen('quit')

    def on_quit(self, event):
        sys.exit()

def run():
    game = Game(
        'Sample',
        (800, 600),
        os.path.join(os.path.dirname(__file__), 'res')
    )
    game.navigator().set_current_view(FirstLevel())
    game.run()

if __name__ == '__main__':
    run()