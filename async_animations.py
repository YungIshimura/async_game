
import asyncio
import curses
import random
from itertools import cycle

from config import CANVAS_SYMBOLS, FloatInt
from curses_tools import draw_frame, read_controls
from tools import check_possibility_of_movement, get_spaceship_animations, get_garbage_animation
from async_tools import sleep
from physics import update_speed


async def fire(canvas: curses.window, rows_speed: FloatInt = -0.3,
               columns_speed: FloatInt = 0) -> None:
    canvas_height, canvas_width = canvas.getmaxyx()
    row, column = canvas_height/2, canvas_width/2

    canvas.addstr(round(row), round(column), '*')
    await sleep()

    canvas.addstr(round(row), round(column), 'O')
    await sleep()

    canvas.addstr(round(row), round(column), ' ')

    row += rows_speed
    column += columns_speed

    symbol = '-' if columns_speed else '|'
    rows, columns = canvas.getmaxyx()
    max_row, max_column = rows - 1, columns - 1

    curses.beep()

    while 0 < row < max_row and 0 < column < max_column:
        canvas.addstr(round(row), round(column), symbol)
        await sleep()
        canvas.addstr(round(row), round(column), ' ')
        row += rows_speed
        column += columns_speed


async def blink(canvas: curses.window, tic: int,symbols: str = CANVAS_SYMBOLS) -> None:
    symbol = random.choice(symbols)
    canvas_height, canvas_width = canvas.getmaxyx()
    row = random.randint(1, canvas_height-2)
    column = random.randint(1, canvas_width-2)

    async def change_brightness(attr):
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
    row_speed = 0
    column_speed = 0

    for animation in cycle(animations):
        row_shift, column_shift, space_pressed = read_controls(canvas)

        if row_shift != 0 or column_shift != 0:
            row_speed, column_speed = update_speed(row_speed, column_speed, row_shift, column_shift)
            new_row, new_column = row + row_speed, column + column_speed
            if check_possibility_of_movement(canvas, new_row, new_column, animation):
                row, column = new_row, new_column    
        else: 
            row_speed = 0
            column_speed = 0

        if space_pressed:
            await fire(canvas)
    
        draw_frame(canvas, row, column, animation)
        await sleep()
        draw_frame(canvas, row, column, animation, True)


async def fly_garbage(canvas,garbage_frame, column, speed=0.5):
    """Animate garbage, flying from top to bottom. Сolumn position will stay same, as specified on start."""
    _, canvas_width = canvas.getmaxyx()

    row = 0

    while row < canvas_width:
        draw_frame(canvas, row, column, garbage_frame)
        await sleep()
        draw_frame(canvas, row, column, garbage_frame, True)
        row += speed


async def fill_orbit_with_garbage(canvas):
    _, canvas_width = canvas.getmaxyx()

    while True:
        column = random.randint(1, canvas_width-2)
        column = max(column, 0)
        column = min(column, canvas_width - 1)

        garbage_frame = get_garbage_animation()
        await fly_garbage(canvas, garbage_frame, column)
        await sleep(5)