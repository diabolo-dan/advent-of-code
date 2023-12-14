
from __future__ import annotations
from pathlib import Path
from collections.abc import Iterator
import attrs

@attrs.frozen
class Index:
    row: int
    column: int


    def neighbours(self) -> set[Index]:
        """neighbours including self."""
        # Includes out of bounds, but that doesn't matter.
        return {Index(self.row + i, self.column + j) for i in range(-1, 2) for j in range(-1, 2)}



def is_symbol(char: str):
    #return not (char.isalnum() or char == '.')
    return char == '*'

def find_symbols(lines: list[str]) -> Iterator[Index]:
    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            if is_symbol(char):
                print(line)
                print(f'{char=}, {i=}, {j=}')
                yield Index(i,j)


@attrs.frozen
class NumberLocation():
    number: int
    end_location: Index

    @property
    def length(self) -> int:
        return len(str(self.number))


    def used_spaces(self) -> set[Index]:
        return {Index(self.end_location.row, self.end_location.column - i) for i in range(self.length) }

def find_numbers(lines: list[str]) -> Iterator[int]:
    current_number = 0
    for row, line in enumerate(lines):
        for column, digit in enumerate(line):
            if digit.isnumeric():
                current_number = current_number * 10 + int(digit)
            elif current_number  != 0:
                yield  NumberLocation(current_number, end_location=Index(row=row, column=column-1))
                current_number = 0
        if current_number != 0:
            yield  NumberLocation(current_number, end_location=Index(row=row, column=len(line)-1))



def process_per_symbol(star_symbols: list[Index], numbers: list[NumberLocation]) -> Iterator[int]:
    for star_symbol in star_symbols:
        star_symbols_for_number = [n.number for n in numbers if n.used_spaces() & star_symbol.neighbours()]
        if len(star_symbols_for_number) ==2:
            a,b = star_symbols_for_number
            yield a*b




def main():
    lines = [l for l in Path('day-3.input').read_text().split('\n') if l]
    symbol_indexes = list(find_symbols(lines))

    all_interesting_indexes = {n for s in  symbol_indexes for n in s.neighbours()}
    print(all_interesting_indexes)
    print(symbol_indexes)
    numbers = list(find_numbers(lines))


    print(numbers)
    relevant_numbers = [n for n in numbers if n.used_spaces() & all_interesting_indexes]
    print (relevant_numbers)
    print(sum(r.number for r in relevant_numbers))

    print(sum(process_per_symbol(symbol_indexes, relevant_numbers)))


main()
