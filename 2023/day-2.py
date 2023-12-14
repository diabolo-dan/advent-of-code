
from pathlib import Path

import attrs

@attrs.frozen
class Pull:
    red: int
    green: int
    blue: int


    def within(self, red: int, green: int, blue: int) -> bool:
        return self.red <= red and self.green <= green and self.blue <= blue

    def power(self):
        return self.red * self.green * self.blue


@attrs.frozen
class Game:
    game_name: int
    pulls: list[Pull]


    @property
    def game_number(self) -> int:
        _, number = self.game_name.split(' ')
        return int(number)

    def within(self, red: int, green: int, blue: int) -> bool:
        return all(p.within(red=red, green=green, blue=blue) for p in self.pulls)

    def minimums(self) -> Pull:
        return Pull(
                red = max(p.red for p in self.pulls),
                green = max(p.green for p in self.pulls),
                blue = max(p.blue for p in self.pulls),
        )


def parse_pull(pull: str) -> Pull:
    pull_colours = [p.strip() for p in pull.split(',')]
    red = 0; green=0; blue=0
    for pull in pull_colours:
        number, colour = pull.split(' ')
        match colour:
            case 'red':
                red = int(number)
            case 'green':
                green = int(number)
            case 'blue':
                blue = int(number)
    return Pull(red=red, green=green, blue=blue)





def parse_game(game: str) -> Game:
    print(game)
    game_name, rest = game.split(':')
    
    pulls = [parse_pull(p) for p in rest.split(';')]

    print(game_name, pulls)
    return Game(game_name=game_name, pulls=pulls)

def main():
    games = [g for g in Path('day-2.input').read_text().split('\n') if g]
    #games = [g for g in Path('day-2.example-input').read_text().split('\n') if g]
    print(games)
    parsed_games = [parse_game(game) for game in games]
    relevant_games = [g for g in parsed_games if g.within(red=12, green=13, blue=14)]
    print([g.game_name for g in relevant_games])
    print(sum([g.game_number for g in relevant_games]))

    minimum_pulls = [g.minimums() for g in parsed_games]
    print(sum(p.power() for p in minimum_pulls))
        

main()
