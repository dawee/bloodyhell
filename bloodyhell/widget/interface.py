from xml.dom.minidom import parse
from bloodyhell.layer import Layer
from bloodyhell.widget import Widget
from bloodyhell.widget.label import Label


class Interface(Layer):

    NODES = {
        'section': Widget,
        'label': Label
    }

    def __init__(self, path):
        print Widget.get_resolution()
        super(Interface, self).__init__(
            position=(0, 0),
            size=Widget.get_resolution()
        )
        self.set_transparent(True)
        self._dom = parse(path)
        self._index = 0
        self._ids = {}
        self._root = self._dom.getElementsByTagName('interface')[0]
        for node in self._root.childNodes:
            self._build_node(node, None)

    def get(self, id):
        return self._ids[id]

    def _build_node(self, node, parent_widget):
        tag_name = None
        try:
            tag_name = node.tagName
        except:
            pass
        if tag_name in Interface.NODES:
            widget = Interface.NODES[node.tagName]()
            if node.getAttribute('id'):
                self._ids[node.getAttribute('id')] = widget
            for attr_name in widget.get_allowed_attributes():
                widget.attr(attr_name, node.getAttribute(attr_name))
            raw_style = node.getAttribute('style')
            for definition in raw_style.split(';'):
                if definition.find(':') != -1:
                    name = definition.split(':')[0].strip()
                    value = definition.split(':')[1].strip()
                    widget.style(name, value)
            if parent_widget is None:
                self.add_layer(widget, self._index)
            else:
                parent_widget.add_layer(widget, self._index)
            for child in node.childNodes:
                self._build_node(child, widget)
            self._index += 1
