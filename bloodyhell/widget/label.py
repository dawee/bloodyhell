import pygame
from bloodyhell.widget import Widget


class Label(Widget):

    def get_allowed_attributes(self):
        return ['text']

    def blit(self):
        self._font = pygame.font.Font('DroidSansMono.ttf', int(self.style('font-size')))
        self._surface = self._font.render(
            self.attr('text'), True, self.get_color(self.style('color'))
        )
        self._screen.blit(
            self._surface, (self._rect.x, self._rect.y)
        )

    def get_color(self, hex_color):
            hexcolor = hex_color.replace('#', '')
            return (
                int(hexcolor[0:2], 16),
                int(hexcolor[2:4], 16),
                int(hexcolor[4:6], 16)
            )
