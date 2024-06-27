import os

TIC_TIMEOUT = 0.1

ROCKET_ANIMATION_PATH = [
        os.path.join(os.getcwd(), 'assets/rocket_assets/rocket_frame_1.txt'),
        os.path.join(os.getcwd(), 'assets/rocket_assets/rocket_frame_2.txt'),
]
GARBAGE_ANIMATION_PATH = [
        os.path.join(os.getcwd(), 'assets/garbage_assets/duck.txt'),
        os.path.join(os.getcwd(), 'assets/garbage_assets/hubble.txt'),
        os.path.join(os.getcwd(), 'assets/garbage_assets/lamp.txt'),
        os.path.join(os.getcwd(), 'assets/garbage_assets/trash_large.txt'),
        os.path.join(os.getcwd(), 'assets/garbage_assets/trash_small.txt'),
        os.path.join(os.getcwd(), 'assets/garbage_assets/trash_xl.txt'),
]

CANVAS_SYMBOLS = '*.+:'
COUNT_STARS = 150

SPACE_KEY_CODE = 32
LEFT_KEY_CODE = 260
RIGHT_KEY_CODE = 261
UP_KEY_CODE = 259
DOWN_KEY_CODE = 258

FloatInt = float | int
