
from bloodyhell.world.camera import Camera


class World(object):

    def __init__(self, root_layer, camera_config):
        self._camera = Camera(
            target=camera_config['target'],
            width=camera_config['width'],
            rect=camera_config['rect'],
            limits=camera_config['limits'],
        )
        self._root_layer = root_layer
        self._chunks = []

    def add(self, chunk, slot):
        chunk.set_camera(self._camera)
        self._chunks.append(chunk)
        self._root_layer.addLayer(chunk.layer(), slot)

    def pre_display_update(self):
        for chunk in self._chunks:
            chunk.update_rect()

    def camera(self):
        return self._camera
