import curses
import random
import time

from async_animations import animate_spaceship, blink, fire
from config import TIC_TIMEOUT, COUNT_STARS
from tools import get_spaceship_animations


def draw(canvas: curses.window) -> None:
    canvas.border()
    canvas.nodelay(True)
    courutines = []
    y, x = curses.window.getmaxyx(canvas)

    frames = get_spaceship_animations()

    for _ in range(COUNT_STARS):
        courutines.append(
            blink(canvas, random.randint(1, y-2), random.randint(1, x-2))
        )

    courutines.append(fire(canvas, y/2, x/2))
    courutines.append(animate_spaceship(canvas, y/2, x/2-2, frames))

    while True:
        for courutine in courutines.copy():
            try:
                courutine.send(None)
            except StopIteration:
                courutines.remove(courutine)
        canvas.refresh()
        time.sleep(TIC_TIMEOUT)


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)
    curses.curs_set(False)
