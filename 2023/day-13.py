

from __future__ import annotations

import heapq
import string
from collections import Counter
from pathlib import Path
from collections.abc import Iterator, Sequence
import attrs
import math
import itertools
from operator import mul
from functools import reduce

import numpy


def hamming_distance(a: Sequence[str], b: Sequence[str]) -> int:
    return len([i for i,j in zip(a,b, strict=True) if i!=j])

def reflections(line: tuple[str, ...]) -> Counter[int]:
    print('==============')
    print(f'line={"".join(line)}')
    results = Counter()
    for index in range(1, len(line)):
        max_distance = min(len(line) - index, index)
        pre_section = line[index-max_distance:index]
        post_section = line[index+max_distance-1:index-1:-1]
        assert len(pre_section) == len(post_section)
        print(f'{"".join(pre_section)} ?= {"".join(post_section)} at {index=}')
        #print(f'{max_distance=}, {index-max_distance=}, {index+max_distance=}')
        results[index] = hamming_distance(pre_section, post_section)

    print('==============')
    print(f'results: {results}')
    return results


def multi_reflections(lines: list[tuple[str, ...]]) -> set[int]:
    print('*********')
    print('\n'.join([''.join(c for c in line) for line in lines]))
    total_smudges = sum([reflections(s) for s in lines], Counter())
    potential_reflections = range(1, len(lines[0]))
    results = {k for k in potential_reflections if total_smudges[k] == 1}
    print(f'results: {results}')
    print('*********')
    return results

def both_ways_reflections(lines: list[tuple[str, ...]]) -> int:
     all_reflections = multi_reflections(lines) | {100 * x for x in multi_reflections(list(zip(*lines)))}
     assert len(all_reflections) == 1
     return all_reflections.pop()


def parse_group(lines: str) -> list[tuple[str, ...]]:
    return [tuple(l) for l in lines.split('\n') if l]

def main():
    #groups = [l for l in Path('day-13.example-input').read_text().split('\n\n')]
    groups = [l for l in Path('day-13.input').read_text().split('\n\n')]
    print(groups)
    parsed_groups = [parse_group(g) for g in groups]
    print(parsed_groups)
    results = [both_ways_reflections(g) for g in parsed_groups]
    print(results)
    print(sum(results))


main()
