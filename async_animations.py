
import asyncio
import curses
import random
from itertools import cycle
from typing import List
from curses_tools import draw_frame, read_controls
from tools import check_possibility_of_movement
from config import CANVAS_SYMBOLS, FloatInt


async def fire(canvas: curses.window, start_row: FloatInt, start_column: FloatInt, rows_speed: FloatInt=-0.3, columns_speed: FloatInt=0) -> None:
    """Display animation of gun shot, direction and speed can be specified."""

    row, column = start_row, start_column

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


async def blink(canvas: curses.window, row: FloatInt, column: FloatInt, symbols: str=CANVAS_SYMBOLS) -> None:
    symbol = random.choice(symbols)

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


async def animate_spaceship(canvas: curses.window, row: FloatInt, column: FloatInt, animations: List[str]) -> None:
    for animation in cycle(animations):
        row_shift, column_shift, _ = read_controls(canvas)

        if row_shift != 0 or column_shift != 0:
            new_row, new_column = row + row_shift, column + column_shift
            if check_possibility_of_movement(canvas, new_row, new_column, animation):
                row, column = new_row, new_column

        draw_frame(canvas, row, column, animation)
        await asyncio.sleep(0)
        draw_frame(canvas, row, column, animation, True)
