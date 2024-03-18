from abc import ABC, abstractmethod
from typing import List, Any, Literal
from .models import (Game,Genre,Console,Developer)
from django.db.models.query import QuerySet
from .iteratorSearchByName import GameList

# i dont know what you want me to do here
# i decided that searching by different game attributes makes 
# more sense than searching by individual genres
# we'd have to make a new strategy every single time a genre would be addded
# and it would severely break everything. this makes more (yet still incredibly little) sense.
# - alex

# all of these take string arguments, just to make life a little easier

class SearchStrategyInterface(ABC):

    ctx : QuerySet

    # just returns the "working query set" of Game elements we'll be sifting through 
    def get_context(self) -> QuerySet:
        if self.ctx is None:
            return Game.objects # Defaults to all game object
        return self.ctx

    @abstractmethod
    def search(self,s:Any) -> GameList: raise NotImplemented # s is the search item

class SearchViaTitle(SearchStrategyInterface):

    ctx : QuerySet

    def __init__(self, ctx : QuerySet = None) -> None:
        self.ctx = ctx

    def search(self,s:str) -> GameList:
        return GameList(games=self.ctx.filter(title__icontains=s).all())
    
class SearchViaGenre(SearchStrategyInterface):

    ctx : QuerySet

    def __init__(self, ctx : QuerySet = None) -> None:
        self.ctx = ctx

    def search(self, s: str) -> GameList:
        return GameList(games=self.ctx.filter(genres__name__icontains=s).all())

class SearchViaConsole(SearchStrategyInterface):

    ctx : QuerySet

    def __init__(self, ctx : QuerySet = None) -> None:
        self.ctx = ctx

    def search(self, s: str) -> GameList:
        return GameList(games=self.ctx.filter(consoles__name__icontains=s).all())
    
class SearchViaDeveloper(SearchStrategyInterface):

    ctx : QuerySet

    def __init__(self, ctx : QuerySet = None) -> None:
        self.ctx = ctx

    def search(self, s: str) -> GameList:
        return GameList(games=self.ctx.filter(developer__name__icontains=s).all())
        
def get_strategy(
    ctx : QuerySet,
    type : Literal['title', 'genre', 'console', 'developer']
) -> SearchStrategyInterface:
    """
        A utility function to return the proper type of strategy based on a string literal.
        This hopefully prevents you from having to import a whole lot of extra classes into core
        code.
    """
    if type == 'title':
        return SearchViaTitle(ctx)
    elif type == 'console':
        return SearchViaConsole(ctx)
    elif type == 'developer':
        return SearchViaDeveloper(ctx)
    elif type == 'genre':
        return SearchViaGenre(ctx)