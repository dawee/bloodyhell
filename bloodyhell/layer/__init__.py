from bloodyhell.eventdispatcher import EventDispatcher
from bloodyhell.layer.rect import Rect


class Layer(EventDispatcher):

    def __init__(self, parent=None, position=(0, 0), size=(0, 0)):
        super(Layer, self).__init__()
        self._parent = parent
        self._rect = Rect(position, size)
        self._cropped_rect = Rect((0, 0), size)
        self._slots = {}
        self._image_id = None
        self._transparent = False

    def set_transparent(self, transparent):
        self._transparent = transparent

    def loader(self):
        from bloodyhell.resourceloader import ResourceLoader
        return ResourceLoader()

    def add_layer(self, layer, slot=0):
        if not slot in self._slots:
            self._slots[slot] = []
        layer.set_parent(self)
        self._slots[slot].append(layer)
        self.add(layer)

    def remove_layer(self, layer_to_remove):
        for slot in self._slots.keys():
            for layer in self._slots[slot]:
                index = 0
                if layer is layer_to_remove:
                    self._slots[slot].pop(index)
                index += 1
        self.remove(layer_to_remove)

    def set_parent(self, parent):
        self._parent = parent

    def on_frame(self, delta):
        for slot in self._slots.keys():
            for layer in self._slots[slot]:
                layer.on_frame(delta)

    def rect(self):
        return self._rect

    def set_cropped_rect(self, cropped_rect):
        self._cropped_rect = cropped_rect

    def set_image(self, image_id):
        self._image_id = image_id

    def fill(self, hexcolor):
        return self
