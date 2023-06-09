import asyncio
import curses
from random import randint

from curses_tools import draw_frame, read_controls
from curses_tools import check_possibility_of_movement


async def blink(canvas, row, column, symbol='*'):
    delay = randint(100, 10000)
    canvas.addstr(row, column, symbol, curses.A_DIM)
    for _ in range(delay):
        await asyncio.sleep(0)

    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        for _ in range(10000):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        for _ in range(5000):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        for _ in range(4000):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        for _ in range(5000):
            await asyncio.sleep(0)


async def animate_spaceship(canvas, row, column, animations):
    while True:
        for animation in animations:
            for i in range(1500):
                row_shift, column_shift, space = read_controls(canvas)
                if i == 1499:
                    draw_frame(canvas, row, column, animation, True)
                    break
                if check_possibility_of_movement(
                        canvas,
                        row + row_shift,
                        column + column_shift,
                        animation
                        ) is False:
                    continue

                if row_shift != 0 or column_shift != 0:
                    draw_frame(canvas, row, column, animation, True)
                    row += row_shift
                    column += column_shift

                    draw_frame(canvas, row, column, animation)
                    continue
                draw_frame(canvas, row, column, animation)
                await asyncio.sleep(0)


async def fire(canvas, start_row, start_column, rows_speed=-0.3, columns_speed=0):
    """Display animation of gun shot. Direction and speed can be specified."""

    row, column = start_row, start_column

    canvas.addstr(round(row), round(column), '*')
    for _ in range(500):
        await asyncio.sleep(0)

    canvas.addstr(round(row), round(column), 'O')
    for _ in range(500):
        await asyncio.sleep(0)
    canvas.addstr(round(row), round(column), ' ')

    row += rows_speed
    column += columns_speed

    symbol = '-' if columns_speed else '|'

    rows, columns = canvas.getmaxyx()
    max_row, max_column = rows - 1, columns - 1

    curses.beep()

    while 1 < row < max_row and 0 < column < max_column:
        canvas.addstr(round(row), round(column), symbol)
        for _ in range(500):
            await asyncio.sleep(0)
        canvas.addstr(round(row), round(column), ' ')
        row += rows_speed
        column += columns_speed