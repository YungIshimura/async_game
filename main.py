import curses
import random
import time

from async_animations import (animate_spaceship, blink,
                              fill_orbit_with_garbage, show_title)
from config import COUNT_STARS, TIC_TIMEOUT, YEAR_DURATION, YEAR
from global_variables import courutines


def draw(canvas: curses.window) -> None:
    global YEAR
    canvas.border()
    canvas.nodelay(True)
    courutines.append(fill_orbit_with_garbage(canvas))

    for _ in range(COUNT_STARS):
        tic = random.randint(1, 20)
        courutines.append(
            blink(canvas, tic)
        )
    courutines.append(animate_spaceship(canvas))

    year_tics = 0

    while True:
        for coroutine in courutines.copy():
            try:
                coroutine.send(None)
            except StopIteration:
                courutines.remove(coroutine)

        year_tics += 1
        if year_tics == YEAR_DURATION:
            courutines.append(show_title(canvas, YEAR))
            year_tics = 0
            YEAR += 1

        canvas.refresh()
        time.sleep(TIC_TIMEOUT)


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)
    curses.curs_set(False)
