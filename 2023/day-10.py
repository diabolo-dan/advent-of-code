

from __future__ import annotations

import heapq
from pathlib import Path
from collections.abc import Iterator
import attrs
import math
import itertools
from operator import mul
from functools import reduce
import shapely

import numpy

@attrs.frozen
class Index:
    row: int
    column: int

    def after_connection(self, c: Connection) -> Index:
        #print(f'{self=}, {c=}')
        return Index(
            column=self.column + c.column,
            row=self.row + c.row
        )

@attrs.frozen
class Connection:
    row: int
    column: int

    def from_index(self, x, y):
        return self.row + x, self.column + y

@attrs.frozen
class Pipe:
    location: Index
    joins: tuple[Connection, Connection]

    def neighbours(self) -> list[Index]:
        return [self.location.after_connection(join) for join in self.joins]



@attrs.frozen
class Start:
    location: Index

    def possible_neighbours(self) -> list[Index]:
        return [self.location.after_connection(join) for join in self.joins]

    @property
    def joins(self) -> list[Connection]:
        return [Connection(1,0), Connection(-1,0), Connection(0,1), Connection(0,-1)]



pipe_connections = {
    '|': (Connection(1, 0), Connection(-1,0)),
    '-': (Connection(0, 1), Connection(0,-1)),
    'F': (Connection(0, 1), Connection(1,0)),
    'L': (Connection(0, 1), Connection(-1,0)),
    '7': (Connection(0, -1), Connection(1,0)),
    'J': (Connection(0, -1), Connection(-1,0)),
}


def process_maze(lines):
    for row, line in enumerate(lines):
        print(row, f'{line=}')
        for column, char in enumerate(line):
            if char in pipe_connections:
                yield Pipe(location=Index(row,column), joins = pipe_connections[char])
            elif char == 'S':
                yield Start(location=Index(row, column))



def maze_points(start_point: Pipe|Start, direction: Index, maze: dict[Index, Pipe|Start]) -> Iterator[Index]:
    last_location = start_point
    current_location: Pipe|Start = maze[direction]
    num_traversed = 1
    #print(f'{start_point.location=}, {direction=}, {current_location.neighbours()=}')
    yield start_point.location
    while current_location != start_point:
        yield current_location.location
        next_indexes = [c for c in current_location.neighbours() if c != last_location.location]
        #print(f'{current_location=}, {next_indexes=}')
        next_index, = next_indexes
        last_location = current_location
        current_location = maze[next_index]
        num_traversed += 1
    return num_traversed

def groupby(l, key, transform):
    return {k: [transform(i) for i in v] for k,v in itertools.groupby(sorted(l, key=key), key=key)}


def internal_points(lines, maze_indexes: list[Index], maze) -> Iterator[Index]:

    shape = shapely.Polygon((i.row, i.column) for i in maze_indexes)

    # horizontals = [i for i in maze_indexes if any( join for join in  maze[i].joins if join.column == 0)]
    # verticals = [i for i in maze_indexes if any( join for join in maze[i].joins if join.row == 0)]
    # column_by_row = groupby(horizontals, lambda i: i.row, lambda i: i.column)
    # row_by_column = groupby(verticals, lambda i: i.column, lambda i: i.row)
    mi = set(maze_indexes)
    for row, line in enumerate(lines):
        for column, _ in enumerate(line):
            i = Index(row, column)
            if  i  in mi:
                continue
            if shape.contains(shapely.Point(row, column)):
                print(i)
                yield  i
            #
            # if column in column_by_row.get(row, []) or row in row_by_column.get(column, []):
            #     continue
            #
            #
            #
            # smaller_column = [c for c in column_by_row.get(row, []) if c < column]
            # larger_column = [c for c in column_by_row.get(row, []) if c > column]
            # smaller_row = [r for r in row_by_column.get(column, []) if r < row]
            # larger_row = [r for r in row_by_column.get(column, []) if r > row]
            #
            # if (len(smaller_column) % 4 != 0 and len(larger_column) %4 != 0) or (len( smaller_row) % 4 != 0 and len(larger_row) %4 != 0):
            #     print(f'++++++')
            #     print(f'{column_by_row.get(row)=}, {row_by_column.get(column)=}')
            #     i = Index(row, column)
            #     print(f'{i=}, {smaller_row=}, {smaller_column=}')
            #     yield i


def main():
#    lines = [l for l in Path('day-10.example-input2').read_text().split('\n') if l]
    lines = [l for l in Path('day-10.input').read_text().split('\n') if l]
    print(lines)
    maze = {pipe.location: pipe for pipe in process_maze(lines)}
    start_point, = [s for s in maze.values() if isinstance(s, Start)]
    print(f'{start_point=}, f{maze=}')
    #assert isinstance(start_point, Start)
    direction_1, direction_2 = [s for s in start_point.possible_neighbours() if s in maze and start_point.location in maze[s].neighbours()]
    maze_indexes = list(maze_points(start_point, direction_1, maze) )

    print(len(maze_indexes) // 2)
    points = list(internal_points(lines, maze_indexes, maze))
    print(points)
    print(len(points))



main()
