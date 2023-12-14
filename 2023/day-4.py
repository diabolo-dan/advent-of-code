
from __future__ import annotations
from pathlib import Path
from collections.abc import Iterator
import attrs



@attrs.frozen
class ScratchCard:
    name: str
    winning_numbers: set[str]
    numbers: set[str]

    @property
    def matching_numbers(self) -> int:
        return len(self.winning_numbers & self.numbers)

    @property
    def points(self) -> int:
        if self.matching_numbers == 0:
            return 0
        return 2**(self.matching_numbers-1)

    @classmethod
    def parse_line(self, line: str) -> ScratchCard:
        name, rest = line.split(':')
        winning_numbers, numbers = rest.split('|')
        return ScratchCard(
                name=name,
                winning_numbers=set(n.strip() for n in winning_numbers.split()),
                numbers=set(n.strip() for n in numbers.split()),
        )





def main():
    #lines = [l for l in Path('day-4.example-input').read_text().split('\n') if l]
    lines = [l for l in Path('day-4.input').read_text().split('\n') if l]
    print(lines)

    cards = [ScratchCard.parse_line(line) for line in lines]
    print(cards)

    print(sum(c.points for c in cards))

    scratchcard_numbers = [1 for i in cards]

    for i, card in enumerate(cards):
        for j in range(1, card.matching_numbers + 1):
            scratchcard_numbers[i + j] += scratchcard_numbers[i]
            print(f'{i=}, {j=}, {card.points=}, {scratchcard_numbers[i]=}')
    print(scratchcard_numbers)
    print(sum(scratchcard_numbers))



main()
