import curses
import random
import time
from async_animations import animate_spaceship, blink, fire, get_garbage_animation, fly_garbage
from config import COUNT_STARS, TIC_TIMEOUT
from async_tools import sleep


courutines = []

async def fill_orbit_with_garbage(canvas):
    _, canvas_width = canvas.getmaxyx()

    while True:
        column = random.randint(1, canvas_width-2)
        column = max(column, 0)
        column = min(column, canvas_width - 1)

        garbage_frame = get_garbage_animation()
        await sleep(10)
        courutines.append(fly_garbage(canvas, garbage_frame, column))


def draw(canvas: curses.window) -> None:
    canvas.border()
    canvas.nodelay(True)

    courutines.append(fill_orbit_with_garbage(canvas))
    for _ in range(COUNT_STARS):
        tic = random.randint(1, 20)
        courutines.append(
            blink(canvas, tic)
        )
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
