

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


def process_sequence(sequence: numpy.ndarray[int]) -> tuple[int, int]:
    first_target, last_target = int(sequence[0]), int(sequence[-1])
    if (sequence == 0).all():
        return first_target, last_target
    else:
        a,b = process_sequence(numpy.diff(sequence))
        return first_target - a, last_target + b



def main():
    #lines = [l for l in Path('day-9.example-input').read_text().split('\n') if l]
    lines = [l for l in Path('day-9.input').read_text().split('\n') if l]
    print(lines)
    sequences = [numpy.asarray([int(n) for n in l.split()]) for l in lines]
    print(sequences)
    start_vals, end_vals  = zip(*[process_sequence(s) for s in sequences])
    print(end_vals)
    print(sum(end_vals))
    print(start_vals)
    print(sum(start_vals))

main()
