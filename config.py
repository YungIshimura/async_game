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

PHRASES = {
    1957: "First Sputnik",
    1961: "Gagarin flew!",
    1969: "Armstrong got on the moon!",
    1971: "First orbital space station Salute-1",
    1981: "Flight of the Shuttle Columbia",
    1998: 'ISS start building',
    2011: 'Messenger launch to Mercury',
    2020: "Take the plasma gun! Shoot the garbage!",
}

EXPLOSION_FRAMES = [
    """\
           (_)
       (  (   (  (
      () (  (  )
        ( )  ()
    """,
    """\
           (_)
       (  (   (
         (  (  )
          )  (
    """,
    """\
            (
          (   (
         (     (
          )  (
    """,
    """\
            (
              (
            (

    """,
]

GAME_OVER_ART = '''
 /$$$$$$                                          /$$$$$$                              
/$$__  $$                                        /$$__  $$                             
| $$  \__/ /$$$$$$  /$$$$$$/$$$$   /$$$$$$       | $$  \ $$ /$$    /$$/$$$$$$   /$$$$$$ 
| $$ /$$$$|____  $$| $$_  $$_  $$ /$$__  $$      | $$  | $$|  $$  /$$/$$__  $$ /$$__  $$
| $$|_  $$ /$$$$$$$| $$ \ $$ \ $$| $$$$$$$$      | $$  | $$ \  $$/$$/ $$$$$$$$| $$  \__/
| $$  \ $$/$$__  $$| $$ | $$ | $$| $$_____/      | $$  | $$  \  $$$/| $$_____/| $$      
|  $$$$$$/  $$$$$$$| $$ | $$ | $$|  $$$$$$$      |  $$$$$$/   \  $/ |  $$$$$$$| $$      
\______/ \_______/|__/ |__/ |__/ \_______/       \______/     \_/   \_______/|__/      
'''

YEAR_DURATION = 15
YEAR = 1957
