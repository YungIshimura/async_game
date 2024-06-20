import curses
import time

from async_animations import animate_spaceship, blink, fire
from config import TIC_TIMEOUT, COUNT_STARS


def draw(canvas: curses.window) -> None:
    canvas.border()
    canvas.nodelay(True)
    courutines = []

    for _ in range(COUNT_STARS):
        courutines.append(
            blink(canvas)
        )
    courutines.append(fire(canvas))
    courutines.append(animate_spaceship(canvas))

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
