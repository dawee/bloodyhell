from bloodyhell.layer import Layer
from bloodyhell.resourceloader import ResourceLoader


class AnimatedLayer(Layer):

    def __init__(self, parent=None, position=(0, 0), size=(0, 0)):
        super(AnimatedLayer, self).__init__(parent, position, size)
        self._frames = {}
        self._frame_index = None

    def set_animation(self, animation_id):
        self._frames = ResourceLoader().get_animation_frames(animation_id)
        self.rewind()

    def rewind(self):
        self._frame_index = self._frames.keys()[0]
        self.set_image(self._frames[self._frame_index])

    def step(self):
        self._frame_index += 1
        if self._frame_index not in self._frames.keys():
            self.rewind()
        else:
            self.set_image(self._frames[self._frame_index])

    def blit(self):
        super(AnimatedLayer, self).blit()
        if self._frame_index is not None:
            self.step()
