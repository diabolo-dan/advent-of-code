

from __future__ import annotations

import heapq
from pathlib import Path
from collections.abc import Iterator
import attrs
import math
import itertools
from operator import mul
from functools import reduce

import numpy

def do_tilt(line: str) -> str:
    sections = line.split('#')
    moved_sections = [''.join(sorted(section, reverse=True)) for section in sections]
    return '#'.join(moved_sections)


def string_zip(lines: list[str]) -> list[str]:
    return [''.join(l) for l in zip(*lines)]


def string_reverse(lines: list[str]) -> list[str]:
    return  [
        ''.join(reversed(l)) for l in lines
    ]

def tilted_west(lines: list[str]) -> list[str]:
    return [do_tilt(line) for line in lines]


def tilted_north(lines:list[str]) -> list[str]:
    return string_zip(tilted_west(string_zip(lines)))


def tilted_south(lines:list[str]) -> list[str]:
    return string_zip(tilted_east(string_zip(lines)))

def tilted_east(lines:list[str]) -> list[str]:
    return string_reverse(tilted_west(string_reverse(lines)) )


def print_dish(lines: list[str]) -> str:
    for line in lines:
        print(line)
    return '\n'.join(lines)

@attrs.frozen
class Dish:
    lines: tuple[str]



    def rotated(self) -> Dish:
        north = tilted_north(self.lines)
        west = tilted_west(north)
        south = tilted_south(west)
        east = tilted_east(south)

        return Dish(lines=tuple(east))


    def count_values(self) -> int:
        lines = self.lines
        length = len(lines)
        per_line = [line.count('O') * (length - i) for i, line in  enumerate(lines)]
        print(f'{per_line=}')
        return sum(per_line)

    def __str__(self) -> str:
        return '\n'.join(self.lines)



def main():
    #lines = [l for l in Path('day-14.example-input').read_text().split('\n') if l]
    lines = [l for l in Path('day-14.input').read_text().split('\n') if l]
    dish =Dish(lines=tuple(lines))
    seen = {}
    dishes = {}
    target_rotations = 1000000000
    for i in range(target_rotations):
        if dish in seen:
            break
        print('==============')
        print(f'rotation: {i}')
        print(dish)
        print('==============')
        seen[dish] = i
        dishes[i] =dish
        dish = dish.rotated()
    print(f'{i=}, {seen[dish]=}')
    rotation = i - seen[dish]
    excess = (target_rotations - i) % rotation
    final_dish_number = seen[dish] + excess
    print(f'{rotation=}, {excess=}, {final_dish_number=}')
    final_dish = dishes[final_dish_number]

    #print(final_dish)
    print(final_dish.count_values())




main()
