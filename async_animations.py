import asyncio
import curses
import random
from itertools import cycle

from config import CANVAS_SYMBOLS, GAME_OVER_ART, PHRASES, FloatInt,  YEAR
from curses_tools import draw_frame, get_frame_size, read_controls
from explosion import explode
from global_variables import (courutines, obstacles,
                              obstacles_in_last_collisions)
from obstacles import Obstacle
from physics import update_speed
from tools import (check_possibility_of_movement, get_garbage_animation,
                   get_garbage_delay_tics, get_spaceship_animations, sleep)


async def show_title(canvas: curses.window, year: int) -> None:
    global YEAR
    YEAR = year

    phrase = ''
    canvas_height, canvas_width = canvas.getmaxyx()
    title_max_length = 50
    start_row = canvas_height - 1
    start_column = canvas_width - title_max_length

    title_window = canvas.derwin(start_row, start_column)
    while True:
        if year in PHRASES:
            phrase = PHRASES[year]
            title = ''
            draw_frame(title_window, 0, 0, title)
        title = f'Year {year} {phrase}'
        draw_frame(title_window, 0, 0, title)
        title_window.refresh()
        await asyncio.sleep(0)
        draw_frame(title_window, 0, 0, title, True)


async def fire(canvas: curses.window, row, column, rows_speed: FloatInt = -0.3,
               columns_speed: FloatInt = 0) -> None:

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
        for obstacle in obstacles:
            if obstacle.has_collision(round(row), round(column)):
                obstacles_in_last_collisions.append(obstacle)
                return None


async def blink(canvas: curses.window, tic: int,
                symbols: str = CANVAS_SYMBOLS) -> None:
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
    global YEAR
    for animation in cycle(animations):
        row_shift, column_shift, space_pressed = read_controls(canvas)
        if row_shift != 0 or column_shift != 0:
            row_speed, column_speed = update_speed(row_speed, column_speed,
                                                   row_shift, column_shift)
            new_row, new_column = row + row_speed, column + column_speed
            if check_possibility_of_movement(canvas, new_row,
                                             new_column, animation):
                row, column = new_row, new_column
        else:
            row_speed = 0
            column_speed = 0

        if space_pressed and YEAR >= 2020:
            courutines.append(fire(canvas, row, column+2))

        draw_frame(canvas, row, column, animation)
        await sleep()
        draw_frame(canvas, row, column, animation, True)
        for obstacle in obstacles:
            if obstacle.has_collision(row, column):
                courutines.append(show_gameover(canvas, round(canvas_height/2),
                                                round(canvas_width/2-50)))
                return None


async def fly_garbage(canvas: curses.window, garbage_frame: str,
                      column: int, speed: FloatInt = 0.5) -> None:
    rows_number, columns_number = canvas.getmaxyx()

    column = max(column, 0)
    column = min(column, columns_number - 1)
    rows_size, columns_size = get_frame_size(garbage_frame)
    row = 0
    center_column = round(column + columns_size / 2)
    obstacle = Obstacle(row, column, rows_size, columns_size)
    obstacles.append(obstacle)

    while row < rows_number:
        if obstacle in obstacles_in_last_collisions:
            obstacles_in_last_collisions.remove(obstacle)
            center_row = round(row + rows_size / 2)
            courutines.append(explode(canvas, center_row, center_column))
            break

        draw_frame(canvas, row, column, garbage_frame)

        await asyncio.sleep(0)
        draw_frame(canvas, row, column, garbage_frame, negative=True)
        row += speed
        obstacle.row = row

    obstacles.remove(obstacle)


async def fill_orbit_with_garbage(canvas: curses.window) -> None:
    _, canvas_width = canvas.getmaxyx()

    while True:
        column = random.randint(1, canvas_width-2)
        column = max(column, 0)
        column = min(column, canvas_width - 1)

        garbage_frame = get_garbage_animation()
        garbage_delay = get_garbage_delay_tics(YEAR)
        if garbage_delay:
            await sleep(garbage_delay)
        courutines.append(fly_garbage(canvas, garbage_frame, column))


async def show_gameover(canvas: curses.window, row: int, column: int) -> None:
    while True:
        draw_frame(canvas, row, column, GAME_OVER_ART)
        await sleep()
