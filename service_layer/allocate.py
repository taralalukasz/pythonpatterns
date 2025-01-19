from domain.model import Batch, OrderLine, OutOfStock
from typing import List

def allocate(line: OrderLine, batches: List[Batch] ) -> str:
    # for b in sorted(batches):
    #     if b.can_allocate(line):
    #         yield b  # Return the value of b
    
    #this is equivalent to above
    try:
        batch = next(b for b in sorted(batches) if b.can_allocate(line))
        batch.allocate(line)
        return batch.reference
    except StopIteration: #StopIteration exception is thrown by next() function, if none of the elements fulfills the requirements
        raise OutOfStock(f"Out of stock for {line.sku}")
