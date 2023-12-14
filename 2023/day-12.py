

from __future__ import annotations

import functools
import heapq
from pathlib import Path
from collections.abc import Iterator
import attrs
import math
import itertools
from operator import mul
from functools import reduce

import numpy





@attrs.frozen
class PuzzleLine:
    record: str
    group_sizes: tuple[int, ...]

    @classmethod
    def from_line(cls, line: str) -> PuzzleLine:
        record, groups = line.split()
        group_sizes = [int(n) for n in groups.split(',')]
        return cls(record, tuple(group_sizes))


    def can_be_group(self) -> bool:
        if len(self.group_sizes) == 0:
            return False
        next_group_size, *_ = self.group_sizes
        record = self.record
        if '.' in record[:next_group_size]:
            return False
        if  len(record) < next_group_size:
            return False
        if len(record) > next_group_size and record[next_group_size] == '#':
            return False
        return True


    @functools.lru_cache(maxsize=10000)
    def solutions(self) -> int:
        print(f'recursed: {self=}')

        if not self.group_sizes and '#' in self.record:
            return 0
        elif not self.group_sizes:
            return 1

        sum = 0
        if self.can_be_group():
            next_group_size, *remaining_group_sizes = self.group_sizes
            sum += PuzzleLine(record=self.record[next_group_size + 1:], group_sizes=tuple(remaining_group_sizes)).solutions()
        if self.record and self.record[0] != '#':
            sum += PuzzleLine(record=str(self.record[1:]), group_sizes=self.group_sizes).solutions()
        return sum

    def times(self, number: int):
        record = '?'.join([self.record for i in range(number)])
        groups = self.group_sizes * number
        return PuzzleLine(record=record, group_sizes=groups)




        #
        # match self.group_sizes, self.record:
        #     case
        #         return 0
        #     case [], record:
        #         return 1

        #     case group, ( '.', remaining_record):
        #         return
        #     case (next_group_size, *remaining_group_sizes), record if self.can_be_group()
        #         return
        #     case (first, *rest), record if record[0] == '#' and '.' not in record[:first] and record[first] != '#':
        #
        # if not self.group_sizes:
        #     return 1
        #
        # next_group_size, *remaining_group_sizes = self.group_sizes
        # if sum(self.group_sizes) + len(self.group_sizes) - 1 > len(self.record):
        #     # Impossible to resolve
        #     return 0
        # else:
        #     #print(f'{self=}, recurse other')
        #     match self.record:
        #         case '.', *rest:
        #             return PuzzleLine(record=tuple(rest), group_sizes=self.group_sizes).solutions()
        #         case re.match('#' + '?|##', *rest if '.' not in rest[:next_group_size-1] and:
        #
        #     if self.record[0] == '#':
        #         other_solutions = 0
        #     else:
        #         other_solutions =
        #     if '.' in self.record[:next_group_size] or (len(self.record) > next_group_size and self.record[next_group_size] == '#'):
        #         immediate_solutions = 0
        #     else:
        #         #print(f'{self=}, recurse immediate {remaining_group_sizes}')
        #         immediate_solutions = PuzzleLine(record=self.record[next_group_size + 1:], group_sizes=tuple(remaining_group_sizes)).solutions()
        #     print(f'return {immediate_solutions} + {other_solutions} ({self=})')
        #     return immediate_solutions + other_solutions
        #
        #
        #
        #
        #
        #
        #

def main():
    #lines = [l for l in Path('day-12.example-input').read_text().split('\n') if l]
    lines = [l for l in Path('day-12.input').read_text().split('\n') if l]
    print(lines)
    parsed_puzzles = [PuzzleLine.from_line(line) for line in lines]
    print(parsed_puzzles)
    multiplied_puzzels = [p.times(5) for p in  parsed_puzzles]
    print(multiplied_puzzels)

    solutions = [p.solutions() for p in multiplied_puzzels]
    print(solutions)
    print(sum(solutions))

main()
