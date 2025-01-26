import domain.model as model
from typing import List
from adapters.repository import AbstractRepository
from domain.model import InvalidSku
from datetime import date
from typing import Optional



##service function should have 
    
def allocate(orderid: str, sku: str, qty: int,
              repo: AbstractRepository, session
    ) -> str:
    batches = repo.list()  #(1)
    line = model.OrderLine(orderid, sku, qty)
    if not is_valid_sku(line.sku, batches):  #(2)
        raise InvalidSku(f"Invalid sku {line.sku}")
    batchref = model.allocate(line, batches)  #(3)
    session.commit()  #(4)
    return batchref

def deallocate(orderid: str, sku: str, qty: int,
                repo: AbstractRepository, session
    ) -> str:
    batches = repo.list()  #(1)
    line = model.OrderLine(orderid, sku, qty)
    if not is_valid_sku(line.sku, batches):  #(2)
        raise InvalidSku(f"Invalid sku {line.sku}")
    batchref = model.deallocate(line, batches)  #(3)
    session.commit()  #(4)
    return batchref

def add_batch(
    ref: str, sku: str, qty: int, eta: Optional[date],
    repo: AbstractRepository, session,
) -> None:
    repo.add(model.Batch(ref, sku, qty, eta))
    session.commit()


def is_valid_sku(sku, batches):
    return sku in {b.sku for b in batches}

