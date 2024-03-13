from collections.abc import Iterator, Iterable
from .models import Game
from typing import List

# I don't know how this searches by name, im just going off the diagram and the refactoring guru site
# nowhere does it state that this searches by name. 
# - alex

class GameListIterator(Iterator):
    
    game_list : "GameList"
    current_index : int
    
    def __init__(self, game_list : "GameList") -> None:
        self.current_index = 0
        self.game_list = game_list

    # Makes this object available in a for-loop
    def __next__(self) -> Game:

        try:
            value = self.game_list[self.current_index]
            self.current_index += 1
        except IndexError:
            raise StopIteration()
        
        return value

class GameList(Iterable):

    games : List[Game]

    def __init__(self, games : List[Game] = []) -> None:
        self.games = games
    
    def add_game(self, g : Game) -> None:
        self.games.append(g)

    def remove_game(self, g : Game) -> None:
        self.games.remove(g)

    def pop_game(self, i : int = 0) -> Game:
        return self.games.pop(i)
    
    def __iter__(self) -> "GameListIterator":
        return GameListIterator(game_list = self)
    
    def __getitem__(self, index : int) -> Game:
        return self.games[index]