

from __future__ import annotations
from pathlib import Path
from collections.abc import Iterator
import attrs
import math
import itertools
from operator import mul
from functools import reduce

def parse_line(l: str) -> list[int]:
    _, numbers = l.split(':')
    #return [int(n.strip()) for n in numbers.split()]
    return [int(''.join([n.strip() for n in numbers.split()]))]

@attrs.frozen
class Game:
    time: int
    distance: int


    def _roots(self) -> float:
        return (self.time**2 - 4*(self.distance + 0.00001)) ** 0.5

    def winners(self) -> int:
        print(self._roots())
        return math.ceil((self._roots() - self.time)/ 2) * 2 +  self.time - 1


def main():
    print(Game(7, 10).winners())
    lines = [parse_line(l) for l in Path('day-6.input').read_text().split('\n') if l]
    #lines = [l for l in Path('day-6.input').read_text().split('\n') if l]
    games =  [Game(t, d) for t,d in zip(*lines)]
    print(f'{games=}')
    print([g.winners() for g in games])
    print(reduce(mul, [g.winners() for g in games], 1))

main()
