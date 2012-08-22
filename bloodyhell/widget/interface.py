from xml.dom.minidom import parse
from bloodyhell.layer import Layer
from bloodyhell.widget import Widget


class Interface(Layer):

    NODES = {
        'section': Widget,
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
        self._root = self._dom.getElementsByTagName('interface')[0]
        for node in self._root.childNodes:
            self._build_node(node, None)

    def _build_node(self, node, parent_widget):
        tag_name = None
        try:
            tag_name = node.tagName
        except:
            pass
        if tag_name in Interface.NODES:
            widget = Interface.NODES[node.tagName]()
            for attr_name in widget.get_allowed_attributes():
                widget.attr(node.getAttribute(attr_name))
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