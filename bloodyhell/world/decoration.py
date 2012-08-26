from bloodyhell.world.chunk import Chunk


class Decoration(Chunk):

    def __init__(self, position, size, image_id):
        super(Decoration, self).__init__(position, size)
        self.layer().set_image(image_id)
