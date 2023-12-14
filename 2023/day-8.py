

from __future__ import annotations

import heapq
from pathlib import Path
from collections.abc import Iterator
import attrs
import math
import itertools
from operator import mul
from functools import reduce



def parse_tree(line: str) -> Tree:
    name, rest = line.split(' = ')
    left, right = rest.strip('()').split(', ')
    return Tree(
        name=name,
        left=left,
        right=right,
    )



@attrs.frozen
class Tree:
    name: str
    left: str
    right: str


@attrs.mutable
class GameState:
    graph: dict[str, Tree]
    current_node: str


    def final_node(self):
        #return self.current_node == 'ZZZ'
        return self.current_node.endswith('Z')

    def make_move(self, direction :str) -> None:
        match direction:
            case 'L':
                self.take_left()
            case 'R':
                self.take_right()
            case _:
                raise Exception(direction)

    def take_left(self):
        self.current_node = self.graph[self.current_node].left

    def take_right(self):
        self.current_node = self.graph[self.current_node].right


    def solutions(self, directions: str):
        solutions = {}
        for count, direction in enumerate(itertools.cycle(directions)):
            #print(f'{self=}, {count=}, {direction=}')
            if self.final_node():
                hash_value = (count % len(directions), self.current_node)
                if hash_value in solutions:
                    # looped
                    break
                solutions[hash_value] = count
            elif count > len(self.graph) * len(directions):
                print('no loop')
                break
            self.make_move(direction)
        offset = solutions[hash_value]
        total_count = count
        initial_solution = sorted(x for x in solutions.values() if x < offset)
        #print(f'{initial_solution=}')

        loop_length = total_count - offset
        print(f'{offset=}, {total_count=}, {loop_length=}')
        remaining_solutions = sorted(x for x in solutions.values() if x >= offset)
        print(f'{len(initial_solution)=}, {len(remaining_solutions)=}')
        print('\n')
        assert len(initial_solution) == 0
        assert len(remaining_solutions) == 1
        assert total_count == 2*offset
        return offset
        #yield from initial_solution
        #print(f'{remaining_solutions=}')
        #for i in itertools.count():
            #for solution in remaining_solutions:
                #yield i * loop_length + solution





def main():
    lines = [l for l in Path('day-8.example-input').read_text().split('\n') if l]
    #lines = [l for l in Path('day-8.input').read_text().split('\n') if l]
    print(lines)

    directions = lines[0]
    print (directions)
    trees = [parse_tree(l) for l in lines[1:]]
    print(trees)

    trees = {
        tree.name: tree for tree in trees
    }
    print(trees)
    count = 0
    states = [GameState(trees, x) for x in trees if x.endswith('A')]
    print(f'{[s.current_node for s in states]=}')
    solutions_per_thing = [s.solutions(directions) for s in states]
    print(solutions_per_thing)
    print(math.lcm(*solutions_per_thing))
    # all_solutions = ( (k, len(list(v))) for k,v in itertools.groupby(heapq.merge(*solutions_per_thing)))
    # for depth,number in all_solutions:
    #     if number >= 4:
    #         print(f'{depth=}, {number=}')
    #     if number == len(solutions_per_thing):
    #         break
    # exit(0)
    # for direction in itertools.cycle(directions):
    #     #print(f'{[s.current_node for s in states]=}, {count=}, {direction=}')
    #     if all(c.final_node() for c in states):
    #         break
    #     count += 1
    #     match direction:
    #         case 'L':
    #             for state in states:
    #                 state.take_left()
    #         case 'R':
    #             for state in states:
    #                 state.take_right()
    #         case _:
    #             raise Exception(direction)
    # print(count)

main()
