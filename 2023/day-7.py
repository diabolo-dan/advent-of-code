

from __future__ import annotations
from pathlib import Path
from collections.abc import Iterator
import attrs
import math
import itertools
from operator import mul
from functools import reduce


number_values = {str(i): i for i in range(2, 10)}
face_values = {
        'T': 10,
        'J': 0,
        'Q': 12,
        'K': 13,
        'A': 14,
}
card_values = number_values | face_values


@attrs.frozen
class Hand:
    cards: tuple[int]
    bid: int

    @property
    def hand_type_rank(self) -> int:
        # 5 of a kind: 7
        # four of a kind: 6
        # full house: 5
        # three of a kind: 4
        # 2 pair: 3
        # pair: 2
        # high card: 1
        relevant_cards = [c for c in self.cards if c !=  0] # filter out jokers
        sorted_cards = sorted(relevant_cards)
        per_card_number = sorted([len(list(v)) for _, v in  itertools.groupby(sorted_cards, lambda x: x)])
        match len(set(relevant_cards)):
            case 0:
                return 7
            case 1:
                #print(f'{sorted_cards=}, five of a kind')
                return 7
            case 2:
                # full house or four of a kind.
                match per_card_number:
                    case 2,3: # full house
                        return 5
                    case 2,2: # Joker makes full house
                        #print(f'{sorted_cards=}, full house')
                        return 5
                    case _: # all other possibilities are can be made into 4 of a kind.
                        return 6
            case 3:
                match per_card_number:
                    case 1,2,2:
                        # two pair
                        return 3
                    case _: # jokers make anything else a triplet.
                        #print(f'{sorted_cards=}, three of a kind')
                        print(f'{sorted_cards=}, three of a kind ({per_card_number=})')
                        return 4
            case 4: # pair
                #print(f'{sorted_cards=}, pair')
                return 2
            case 5: # high card
                #print(f'{sorted_cards=}, high card')
                return 1



    @property
    def old_hand_type_rank(self) -> int:
        # 5 of a kind: 7
        # four of a kind: 6
        # full house: 5
        # three of a kind: 4
        # 2 pair: 3
        # pair: 2
        # high card: 1
        sorted_cards = sorted(self.cards)
        match len(set(self.cards)):
            case 1:
                #print(f'{sorted_cards=}, five of a kind')
                return 7
            case 2:
                # full house or four of a kind.
                if sorted_cards[1] == sorted_cards[3]:
                    #print(f'{sorted_cards=}, four of a kind')
                    # four of a kind
                    return 6
                else:
                    #print(f'{sorted_cards=}, full house')
                    # full house
                    return 5
            case 3:
                # three of a kind or 2 pair
                per_card_number = [len(list(v)) for _, v in  itertools.groupby(sorted_cards, lambda x: x)]
                if [n for n in per_card_number if n == 3] != []:
                    #three of a kind
                #    print(f'{sorted_cards=}, three of a kind')
                    return 4
                else:
                #    print(f'{sorted_cards=}, two pair')
                    return 3
            case 4: # pair
                #print(f'{sorted_cards=}, pair')
                return 2
            case 5: # high card
                #print(f'{sorted_cards=}, high card')
                return 1

def parse_line(l: str) -> list[int]:
    hand, bid = l.split()
    cards = [card_values[c] for c in hand]
    return Hand(
            cards = tuple(cards),
            bid =int(bid),
            )


def main():
    #lines = [l for l in Path('day-7.example-input').read_text().split('\n') if l] 
    lines = [l for l in Path('day-7.input').read_text().split('\n') if l]
    print(lines)
    hands = [parse_line(l) for l in lines]
    print(hands)
    print([h.hand_type_rank for h in hands])
    ranked_hands = sorted(hands, key=lambda hand: (hand.hand_type_rank, hand.cards))
    length = len(ranked_hands)

    #for i, hand in enumerate(ranked_hands):
        #print(f'{i + 1}: {hand.cards} ({hand.hand_type_rank})')
    
    #print([((length -i), hand.bid) for i, hand in enumerate(ranked_hands)])
    print(sum([(i+ 1) * hand.bid for i, hand in enumerate(ranked_hands)]))

main()
