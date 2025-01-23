from dataclasses import dataclass
from datetime import date
from typing import Optional

#it's called VALUE OBJECT 
#works like hashcode/equals contract  
#generates constructors 
#FROZEN makes object immutable,
@dataclass(frozen=True) 
class OrderLine:
    orderid: str
    sku: str
    qty: int

@dataclass(frozen=True) 
class Line:
    sku: str
    qty: int

class OutOfStock(Exception):
    pass

class InvalidSku(Exception):
    pass

#it's called ENTITY OBJECT 
#it has unique identifier and functions
#is mutable 
#on ENTITY it's important to implement __hash__ and __eq__
#you should not use entity in a Set or Dict Key
#The hash of an object must never change during its lifetime.
class Batch:
    def __init__(self, ref: str, sku: str, qty: int, eta: Optional[date]):  
        self.reference = ref
        self.sku = sku
        self.eta = eta
        self._purchased_quantity = qty
        self._allocations = set()
    
    #implementing this makes it possible to use sorted() on Batch class object 
    def __gt__(self, other: 'Batch'):
        if self.eta == None:
            return False
        if other.eta is None:
            return True
        return self.eta > other.eta

    def allocate(self, line: OrderLine):  
        if self.can_allocate(line):
            self._allocations.add(line)

    def deallocate(self, line: OrderLine):  
        if line in self._allocations:
            self._allocations.remove(line)
    
    def can_allocate(self, line: OrderLine) -> bool:
        return self.sku == line.sku and self.available_quantity >= line.qty

    @property
    def allocated_quantity(self) -> int:
        return sum(line.qty for line in self._allocations)

    @property
    def available_quantity(self) -> int:
        return self._purchased_quantity - self.allocated_quantity
    
    def __eq__(self, other):
        if not isinstance(other, Batch):
            return False
        return other.reference == self.reference

    #hash is used to identify unique objects in sets or dictionary keys
    def __hash__(self):
        return hash(self.reference)

@dataclass(frozen=True)
class Money:
    currency : str
    value : int

    #you can override +-*/ behavior by defining these methods below. 

    def __add__(self, other) -> 'Money':  # 'Money' instead of Money has to be used, because Money class isn't fully defined at this point. So we need to use "foward reference" by wrapping it with 'Money'
        if self.currency != other.currency:
            raise ValueError(f"cannot add {self.currency} to {other.currency}")
        return Money(self.currency, self.value + other.value)

    def __sub__(self, other) -> 'Money': 
        if self.currency != other.currency:
            raise ValueError(f"cannot subtract {self.currency} to {other.currency}")
        if self.value < other.value:
            raise ValueError(f"cannot subtract higher value from lower value")
        return Money(self.currency, self.value - other.value)
    
    def __mul__(self, other) -> 'Money': 
        if isinstance(other, int):
            return Money(self.currency, self.value * other)
        if self.currency != other.currency:
            raise ValueError(f"cannot subtract {self.currency} to {other.currency}")
        return Money(self.currency, self.value * other.value)
    

@dataclass(frozen=True)
class Name:
    first_name: str
    surname: str

class Person:
    def __init__(self, name: Name):
        self.name = name



