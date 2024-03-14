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

class StockObserver(object):

    changed_stock_state : GameConsoleStock
    subscribers : List["SubscriberInterface"]

    def __init__(self) -> None:
        self.subscribers = []

    def subscribe(self, s : "SubscriberInterface") -> None:
        self.subscribers.append(s)

    def unsubscribe(self, s : "SubscriberInterface") -> None:
        self.subscribers.remove(s)

    def notify_subscribers(self) -> None:
        """Actually iterate over each of the subscribers and send them the new updated stock"""
        for s in self.subscribers:
            s.update(self.changed_stock_state)

    # NOTE: This should be called whenever the GameConsoleStock is reduced by natural causes (e.g., a game sale)
    def item_sell_callback(self, s : GameConsoleStock):
        """The callback to notify subscribers of a stock being reduced"""
        self.changed_stock_state = s    # Set the state to focus on the changed stock
        self.notify_subscribers()   # Notify subscribers


class SubscriberInterface(ABC):

    @abstractmethod
    def update(self, stock : GameConsoleStock) -> None:
        raise NotImplemented


class RestockSubscriber(SubscriberInterface):
    """
        If the stock reaches the set threshold, this subscriber 
        will flag them in the GameConsoleStock model to be displayed.
    """

    def __init__(self, *, threshold: int = 10) -> None:
        self.threshold = threshold

    def update(self, stock: GameConsoleStock) -> None:
        if stock.stock <= self.threshold:
            stock.is_low_stock = True
        else:
         stock.is_low_stock = False
        stock.save()
