

from __future__ import annotations
from pathlib import Path
from collections.abc import Iterator
import attrs
from intervaltree import IntervalTree
import itertools

def parse_seeds(raw_seeds: str) -> Mapping:
    it = IntervalTree()

    seeds = [int(x.strip()) for x in raw_seeds.split()[1:]]
    for start, length in itertools.batched(seeds, 2):
        it[start:start+length] = start
    return Mapping(name='seed', mapping=it)

def parse_maps(lines: list[str]) -> dict[str, Mapping]:
    maps = {}
    lines_to_parse = lines
    while lines_to_parse:
        line = lines_to_parse[0]
        assert ':' in line, line
        from_type, to_type = parse_header(line)
        print(f'{from_type=}, {to_type=}')
        mapping, lines_to_parse = parse_out_mapping(lines_to_parse[1:])

        maps[from_type] = Mapping(name=to_type, mapping=mapping)
        print(maps[from_type])
    return maps



@attrs.frozen
class Mapping:
    name: str
    mapping: IntervalTree[int]

    def intersections(self, other: Mapping):
        return [(a,b) for a in self.mapping for b in other.mapping if (a.overlaps(b))]

    def flatten_with(self, other:Mapping):
        new_mapping = self.mapping.copy()
        for interval in self.mapping:
            #print(f'{interval=}')
            target = interval.data
            length = interval.length()
            for other_interval in other.mapping[target: target+length]:
                #print(f'{target=}, {target+length=}, {other_interval=}')
                start, end, target = new_difference(interval, other_interval)
                new_mapping.chop(start,end)
                new_mapping[start:end] = target
        return Mapping(name=other.name, mapping=new_mapping)


    def lookup(self, i: int) -> int:
        data = self.mapping[i]
        if len(data) == 0:
            return i
        else:
            assert len(data) == 1
            interval, = data
            target_start = interval.data
            source_start = interval.begin
            offset = i - source_start
            return target_start + offset
            
            
        return self.mapping.get(i, i)



def new_difference(source: Interval, target: Interval):
    print(f'{source=}, {target=}')
    new_start = source.begin + max(0, target.begin - source.data)
    new_target = target.data + max(0, source.data-target.begin)
    new_end = source.end -  max(0,  source.data+source.length() - target.end )


    print(f'{new_start=}, {new_end=}, {new_target=}')
    return new_start, new_end, new_target




def parse_header(line: str) -> tuple[str, str]:
    return line[:-5].split('-to-')

def parse_out_mapping(lines: list[str]) -> tuple[Mapping[int, int], list[str]]:
    processed_tuples = []
    for line in lines:
        if ':' in line:
            break
        processed_tuples.append(int(i) for i in line.split())

    mapping = IntervalTree()
    for target_start, source_start, length in processed_tuples:
        mapping[source_start:source_start+length] = target_start
    return mapping, lines[len(processed_tuples):]

def find_location(seed: int, maps: dict[str, Mapping]) -> int:
    current_form = 'seed'
    current_value = seed
    while current_form != 'location':
        m = maps[current_form]
        current_form = m.name
        current_value = m.lookup(current_value)
    return current_value



def main():
    lines = [l for l in Path('day-5.example-input').read_text().split('\n') if l]
    lines = [l for l in Path('day-5.input').read_text().split('\n') if l]
    raw_seeds, *rest = lines
    seeds = parse_seeds(raw_seeds)
    print(seeds)
    maps = parse_maps(rest)
    current_map = seeds
    for k,m in maps.items():
        assert k == current_map.name
        print('...'*10)
        print(f'flattning:\n{current_map}\n\twith\n{m}')
        current_map = current_map.flatten_with(m)
        print(f'result:\n{current_map}')
        print('...'*10)
    print(current_map)

    print(current_map.mapping.begin)
    print(min(v.data for v in current_map.mapping))

    #locations = (find_location(seed, maps) for seed in seeds)
    #print(locations)
    #print(min(locations))


main()
