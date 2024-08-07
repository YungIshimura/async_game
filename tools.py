import asyncio
import curses
import os
import random
from typing import List, Tuple

from config import GARBAGE_ANIMATION_PATH, ROCKET_ANIMATION_PATH, FloatInt


def get_frame_size(text: str) -> Tuple[int, int]:

    lines = text.splitlines()
    rows = len(lines)
    columns = max([len(line) for line in lines])

    return rows, columns


def check_possibility_of_movement(canvas: curses.window, row: FloatInt,
                                  column: FloatInt, animation: str) -> bool:
    canvas_rows, canvas_columns = canvas.getmaxyx()
    border = 1
    frame_rows, frame_columns = get_frame_size(animation)
    max_row = canvas_rows - border - frame_rows
    max_column = canvas_columns - border - frame_columns

    if not (border <= row <= max_row and border <= column <= max_column):
        return False

    return True


def load_file(path: str) -> str | None:
    if not os.path.exists(path):
        return None
    with open(path, 'r') as file_handler:
        animation_file = file_handler.read()

    return animation_file


def get_spaceship_animations() -> List:
    animations = []
    for path_to_animation in ROCKET_ANIMATION_PATH:
        animation = load_file(path_to_animation)
        if animation:
            animations.extend([animation, animation])

    return animations


def get_garbage_animation() -> str:
    trash_animation = random.choice(GARBAGE_ANIMATION_PATH)
    animation = load_file(trash_animation)

    return animation


def get_garbage_delay_tics(year: int) -> int:
    if year < 1961:
        return 30
    elif year < 1969:
        return 20
    elif year < 1981:
        return 14
    elif year < 1995:
        return 10
    elif year < 2010:
        return 8
    elif year < 2020:
        return 6
    else:
        return 2


async def sleep(tics: int = 1) -> None:
    for _ in range(tics):
        await asyncio.sleep(0)
