from abc import ABC, abstractmethod

# Creating the builder that will be used to build the receipt based on cart contents.
class ReceiptBuilder(ABC):
    
    @abstractmethod
    def add_item(self, item):
        pass
    
    @abstractmethod
    def set_footer(self, footer):
        pass
    
    @abstractmethod
    def get_receipt(self):
        pass

# Defining the receipt contents that the builder will use.
class Receipt:
    
    def __init__(self):
        self.items = []
        self.total_cost = 0
        self.footer = ""
    
    def add_item(self, item):
        self.items.append(item)
        self.total_cost += item['cost']
    
    def set_footer(self, footer):
        self.footer = footer

# Implementation of the concrete builder method to create receipts.        
class DetailedReceiptBuilder(ReceiptBuilder):
    
    def __init__(self):
        self.receipt = Receipt()
    
    def add_item(self, item):
        self.receipt.add_item(item)
    
    def set_footer(self, footer):
        self.receipt.set_footer(footer)
    
    def get_receipt(self):
        return self.receipt

# The Director that is reponsible for executing the building steps of the receipt.
# Technically optional but the Refactoring.guru Python example uses one.
    
class ReceiptDirector:
    
    def __init__(self, builder):
        self._builder = builder
    
    def construct_receipt(self, items, footer):
        for item in items:
            self._builder.add_item(item)
        self._builder.set_footer(footer)
    
    def get_receipt(self):
        return self._builder.get_receipt()