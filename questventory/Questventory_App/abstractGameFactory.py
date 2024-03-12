from abc import ABC, abstractmethod
from django.db import transaction
from .models import Game, Console, Developer, Genre, GameConsoleStock

# The abstract factory instantiation for creating new game entries.
class AbstractGameInventoryFactory(ABC):
    @abstractmethod
    def create_game(self, title, release_date, developer_name, genre_ids, console_ids, stock):
        pass

    
class GameInventoryFactory(AbstractGameInventoryFactory):
    # Atomic transaction makes sure that all the fields are valid before creating anything.
    # Nothing will be done if a field is not valid.
    @transaction.atomic
    def create_game(self, title, release_date, developer_name, genre_ids, console_ids, stock):
        # Create or get the Developer
        developer, _ = Developer.objects.get_or_create(name=developer_name)

        # Create the Game
        game = Game.objects.create(title=title, release_date=release_date, developer=developer)

        # Associate Genres
        genres = Genre.objects.filter(id__in=genre_ids)
        game.genres.set(genres)

        # Associate Consoles and Stock
        for console_id in console_ids:
            console = Console.objects.get(id=console_id)
            GameConsoleStock.objects.create(game=game, console=console, stock=stock)

        return game
