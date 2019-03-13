from common.colors import get_color


class Colorable(object):
    def __init__(self, color='black'):
        self.color = get_color(color)

    def set_color(self, color):
        self.color = get_color(color)
