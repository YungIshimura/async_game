import curses
from tools import get_star_coroutines
from tools import get_fire_animation_coroutine
from tools import get_spaceship_animation_coroutine


TIC_TIMEOUT = 0.1


def draw(canvas):
    canvas.border()
    curses.curs_set(False)
    canvas.nodelay(True)

    coroutines = get_star_coroutines(canvas)
    coroutines.append(get_fire_animation_coroutine(canvas))
    # animate_spaceship_coroutine = get_spaceship_animation_coroutine(canvas)
    # coroutines.append(animate_spaceship_coroutine)

    while True:
        for courutine in coroutines.copy():
            try:
                courutine.send(None)     
            except StopIteration:
                coroutines.remove(courutine)
        canvas.refresh()


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)