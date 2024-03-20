from typing import List
from abc import ABC, abstractmethod
from .models import GameConsoleStock

# The UML Diagram states:
# An "Inventory" shall have a list of 'subscribers'
# A subscriber has an "updateItem(count)" method
# Individual Items inherit this method (this wont work with the current implementation)
# as each game in the database is not an actual individual object and is data-driven.

# An alternative to this could be:
# The StockObserver shall have a list of "subsribers"
# A subscriber has an "update(stock : GameConsoleStock)" method
# A subscriber will handle protocols to manage and maintain stock.
# or alternatively, deal with other procedures branching off the change in stock

# this doesn't deal with individual games, but rather a process using game stocks
# which lets us focus on those objects, and operate based on both a stock integer 
# and game data, which is probably more "useful"

class LowStockNotification:
    def __init__(self, game_id, console_id, game_title, console_name, stock_amount):
        self.game_id = game_id
        self.console_id = console_id
        self.game_title = game_title
        self.console_name = console_name
        self.stock_amount = stock_amount

class StockObserver:

    instance : "StockObserver" # The singleton instance

    def __init__(self) -> None:
        self.subscribers: List["SubscriberInterface"] = []
        self.low_stock_notifications: List[LowStockNotification] = []

    def subscribe(self, s : "SubscriberInterface") -> None:
        self.subscribers.append(s)

    def unsubscribe(self, s : "SubscriberInterface") -> None:
        self.subscribers.remove(s)

    def notify_subscribers(self, stock: GameConsoleStock) -> None:
        """Actually iterate over each of the subscribers and notify them of low stock items"""
        for s in self.subscribers:
            s.update(stock)

    # NOTE: This should be called whenever the GameConsoleStock is reduced by natural causes (e.g., a game sale)
    def item_sell_callback(self, stock:  GameConsoleStock) -> None:
        """The callback to notify subscribers of a stock being reduced"""
        self.notify_subscribers(stock)
    
    # Adding a low stock notification where necessary.    
    def add_low_stock_notification(self, notification: LowStockNotification) -> None:
        # For/If statements here check to see if a notification for a particular game/console
        # already exists. If it doesn't, it gets added. If it does, nothing happens.
        for existing_notification in self.low_stock_notifications:
            if (existing_notification.game_id == notification.game_id and
                existing_notification.console_id == notification.console_id):
                return
        self.low_stock_notifications.append(notification)

    # Getting low stock notifications to display where needed.
    def get_low_stock_notifications(self) -> List[LowStockNotification]:
        return self.low_stock_notifications

    @classmethod
    def get_instance(cls):
        if not hasattr(cls, "instance"):
            cls.instance = StockObserver()
        return cls.instance

class SubscriberInterface(ABC):

    @abstractmethod
    def update(self, stock : GameConsoleStock) -> None:
        raise NotImplemented


# This is the subscriber that receives notifications for low stock items. Currently
# the low stock threshold is 10, but it could be changed to anything.
class LowStockSubscriber(SubscriberInterface):
    def __init__(self, observer: StockObserver, threshold: int = 10) -> None:
        self.observer = observer
        self.threshold = threshold
    
    def update(self, stock: GameConsoleStock) -> None:
        if stock.stock <= self.threshold:
            notification = LowStockNotification(
                game_id=stock.game.id,
                console_id=stock.console.id,
                game_title=stock.game.title,
                console_name=stock.console.name,
                stock_amount=stock.stock
            )
            self.observer.add_low_stock_notification(notification)
            print("Notification added.")
