
import asyncio
import curses
import random
from itertools import cycle
from curses_tools import draw_frame, read_controls
from tools import check_possibility_of_movement, get_spaceship_animations
from config import CANVAS_SYMBOLS, FloatInt


async def fire(canvas: curses.window, rows_speed: FloatInt = -0.3,
               columns_speed: FloatInt = 0) -> None:
    """Display animation of gun shot, direction and speed can be specified."""

    canvas_height, canvas_width = canvas.getmaxyx()
    row, column = canvas_height/2, canvas_width/2

    canvas.addstr(round(row), round(column), '*')
    await asyncio.sleep(0)

    canvas.addstr(round(row), round(column), 'O')
    await asyncio.sleep(0)
    canvas.addstr(round(row), round(column), ' ')

    row += rows_speed
    column += columns_speed

    symbol = '-' if columns_speed else '|'

    rows, columns = canvas.getmaxyx()
    max_row, max_column = rows - 1, columns - 1

    curses.beep()

    while 0 < row < max_row and 0 < column < max_column:
        canvas.addstr(round(row), round(column), symbol)
        await asyncio.sleep(0)
        canvas.addstr(round(row), round(column), ' ')
        row += rows_speed
        column += columns_speed


async def blink(canvas: curses.window, symbols: str = CANVAS_SYMBOLS) -> None:
    symbol = random.choice(symbols)
    canvas_height, canvas_width = canvas.getmaxyx()
    row = random.randint(1, canvas_height-2)
    column = random.randint(1, canvas_width-2)

    async def change_brightness(attr):
        tic = random.randint(1, 20)
        canvas.addstr(row, column, symbol, attr)
        for _ in range(tic):
            await asyncio.sleep(0)

    while True:
        await change_brightness(curses.A_DIM)
        await change_brightness(0)
        await change_brightness(curses.A_BOLD)
        await change_brightness(0)


async def animate_spaceship(canvas: curses.window) -> None:
    animations = get_spaceship_animations()
    canvas_height, canvas_width = canvas.getmaxyx()
    row = canvas_height / 2
    column = canvas_width / 2 - 2

    for animation in cycle(animations):
        row_shift, column_shift, _ = read_controls(canvas)

        if row_shift != 0 or column_shift != 0:
            new_row, new_column = row + row_shift, column + column_shift
            if check_possibility_of_movement(canvas, new_row, new_column, animation):
                row, column = new_row, new_column

        draw_frame(canvas, row, column, animation)
        await asyncio.sleep(0)
        draw_frame(canvas, row, column, animation, True)
