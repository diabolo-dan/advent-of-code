

from __future__ import annotations

import itertools
from collections.abc import Iterator
from pathlib import Path

import attrs


def expand_one_way(lines: Iterator[str]) -> Iterator[str]:
    for line in lines:
        if '#' not in line:
            yield line
        yield line

def expand_lines(lines: list[str]) -> list[str]:
    return [''.join(l) for l in
            expand_one_way(
                zip(
                    *expand_one_way(
                        zip(*lines)
                    )
                )
            )
    ]


def extract_galaxy_coordinates(expanded: list[str]) -> list[Index]:
    for i, line in enumerate(expanded):
        for j, char in enumerate(line):
            if char == '#':
                yield Index(row=i, column=j)


@attrs.frozen
class Index:
    row: int
    column: int

    def __sub__(self, other: Index) -> int:
        return abs(self.row - other.row) + abs(self.column - other.column)


@attrs.frozen
class EmptyGalaxies:
    rows: list[int]
    columns: list[int]

    def difference(self, i: Index, j: Index) -> int:
        row_galaxies = len([r for r in self.rows if (i.row < r < j.row) or (j.row < r < i.row)])
        column_galaxies = len([c for c in self.columns if (i.column < c < j.column) or (j.column < c < i.column)])
        return i - j + (row_galaxies + column_galaxies) * (10**6 - 1)



def main():
    #lines = [l for l in Path('day-11.example-input').read_text().split('\n') if l]
    lines = [l for l in Path('day-11.input').read_text().split('\n') if l]
    print(lines)
    #expanded = expand_lines(lines)
    empty_rows = [i for i, row in enumerate(lines) if '#' not in row]
    empty_columns = [i for i, column in enumerate(zip(*lines)) if '#' not in column]
    galaxies = extract_galaxy_coordinates(lines)

    empties = EmptyGalaxies(rows=empty_rows, columns=empty_columns)

    diffs =[ empties.difference(galaxy_a, galaxy_b) for galaxy_a, galaxy_b in itertools.product(galaxies, repeat=2)]
    print(diffs)
    print(sum(diffs) / 2)




main()
