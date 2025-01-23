from domain.model import Batch, OrderLine, OutOfStock
from typing import List
from adapters.repository import AbstractRepository
from domain.model import InvalidSku

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

# def allocate(line: OrderLine, repo: AbstractRepository, session) -> str:
#     batches = repo.list()
#     if not is_valid_sku(line.sku, batches):
#         raise InvalidSku(f"Invalid sku {line.sku}")
#     batchref = allocate(line, batches)
#     session.commit()
#     return batchref

# def is_valid_sku(sku, batches):
#     return sku in {b.sku for b in batches}