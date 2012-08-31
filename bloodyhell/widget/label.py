from bloodyhell.widget import Widget


class Label(Widget):

    def get_allowed_attributes(self):
        return ['text']

    def get_color(self, hex_color):
            hexcolor = hex_color.replace('#', '')
            return (
                int(hexcolor[0:2], 16),
                int(hexcolor[2:4], 16),
                int(hexcolor[4:6], 16)
            )
