BLUE_LIGHT = '#0080ff'
BLUE = '#2c5dcd'
GREEN = '#00cc66'
GREEN_LIGHT = '#ccffcc'
GREEN_NEON = '#00cc00'
GREY = '#aaaaaa'
GREY_LIGHT = '#cbcbcb'
GREY_DARK = '#4d4d4d'
PURPLE = '#5918bb'
RED = '#cc0000'
RED_DARK = '#c5060b'
RED_LIGHT = '#ffcccc'
RED_BRIGHT = '#ff0000'
WHITE = '#ffffff'
TURQUOISE = '#318495'
ORANGE = '#ff8000'
YELLOW = '#ffff00'
BLACK = '#000000'
DEFAULT = BLACK

COLORS = {
    'blue_light': BLUE_LIGHT,
    'blue': BLUE,
    'green': GREEN,
    'green_light': GREEN_LIGHT,
    'green_neon': GREEN_NEON,
    'grey': GREY,
    'grey_light': GREY_LIGHT,
    'grey_dark': GREY_DARK,
    'purple': PURPLE,
    'red': RED,
    'red_dark': RED_DARK,
    'red_light': RED_LIGHT,
    'red_bright': RED_BRIGHT,
    'white': WHITE,
    'turquoise': TURQUOISE,
    'orange': ORANGE,
    'yellow': YELLOW,
    'default': BLACK
}


def get_color(color='default'):
    return COLORS.get(color, color)
