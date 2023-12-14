
from collections.abc import Sequence
from pathlib import Path



name_mappings = {
        'one': 1,
        'two': 2,
        'three': 3,
        'four': 4,
        'five': 5,
        'six': 6,
        'seven': 7,
        'eight': 8,
        'nine': 9,
}

numeral_mappings = {str(i): i for i in range(10)}

all_mappings = name_mappings | numeral_mappings




def extract_digits(line: str) -> Sequence[int]:
    digits = []
    remaining = line
    while remaining:
        for name in all_mappings:
            if remaining.startswith(name):
                digits.append(all_mappings[name])
                remaining = remaining[1:]
                break
        else:
            remaining = remaining[1:]
    return digits


def process_line(line: str) -> int:
    digits = extract_digits(line)
    first_digit = digits[0]
    last_digit = digits[-1]
    result = first_digit * 10 + last_digit 
    print(f'{line=}, {digits=}, result={result}')
    return  result


def main():
    lines = [l for l in Path('day-1.input').read_text().split('\n') if l]
    return sum([process_line(line) for line in lines])

    ...

if __name__ == '__main__':
    #print(extract_digits('twone'))
    print(main())
