

class InitRectException(Exception):
    pass


class Rect(object):

    def __init__(self, *args):
        if len(args) == 0:
            self.x = 0
            self.y = 0
            self.width = 0
            self.height = 0
        elif len(args) == 1 and type(args[0]) == tuple:
            self.x, self.y = args[0]
            self.width = 0
            self.height = 0
        elif len(args) == 2 \
                       and type(args[0]) == tuple \
                       and type(args[1]) == tuple:
            self.x, self.y = args[0]
            self.width, self.height = args[1]
        elif len(args) == 4:
            self.x = args[0]
            self.y = args[1]
            self.width = args[2]
            self.height = args[3]
        else:
            raise InitRectException('Rect : bad arguments')
        self.left = self.x
        self.right = self.x + self.width
        self.top = self.y
        self.bottom = self.y + self.height
