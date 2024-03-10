from abc import ABC, abstractmethod
from .models import Game, Console, Developer, Genre, GameConsoleStock

# Defining abstract methods
class AbstractGameInventoryFactory(ABC):
    @abstractmethod
    def create_game(self, **kwargs):
        pass

    @abstractmethod
    def create_console(self, **kwargs):
        pass

    @abstractmethod
    def create_developer(self, **kwargs):
        pass

    @abstractmethod
    def create_genre(self, **kwargs):
        pass

    @abstractmethod
    def manage_game_stock(self, game_id, console_id, stock):
        pass
    
# Concrete Implementation of the Abstract Game Factory Design pattern
# to add games to the Database.

class GameInventoryFactory(AbstractGameInventoryFactory):
    def create_game(self, **kwargs):
        return Game.objects.create(**kwargs)

    def create_console(self, **kwargs):
        return Console.objects.create(**kwargs)

    def create_developer(self, **kwargs):
        return Developer.objects.create(**kwargs)

    def create_genre(self, **kwargs):
        return Genre.objects.create(**kwargs)

    def manage_game_stock(self, game_id, console_id, stock):
        game_instance = Game.objects.get(id=game_id)
        console_instance = Console.objects.get(id=console_id)
        stock_entry, created = GameConsoleStock.objects.get_or_create(
            game=game_instance, 
            console=console_instance, 
            defaults={'stock': stock}
        )
        if not created:
            # Checks if the game already exists and has stock. If it does, it'll add
            # to the existing stock.
            stock_entry.stock = stock
            stock_entry.save()
        return stock_entry
