import domain.model as model
from typing import List
from adapters.repository import AbstractRepository
from domain.model import InvalidSku



##service function should have 

def allocate(line: model.OrderLine, repo: AbstractRepository, session) -> str:
    batches = repo.list()  #(1)
    
    if not is_valid_sku(line.sku, batches):  #(2)
        raise InvalidSku(f"Invalid sku {line.sku}")
    batchref = model.allocate(line, batches)  #(3)
    session.commit()  #(4)
    return batchref

def deallocate(line: model.OrderLine, repo: AbstractRepository, session) -> str:
    batches = repo.list()  #(1)
    if not is_valid_sku(line.sku, batches):  #(2)
        raise InvalidSku(f"Invalid sku {line.sku}")
    batchref = model.deallocate(line, batches)  #(3)
    session.commit()  #(4)
    return batchref


def is_valid_sku(sku, batches):
    return sku in {b.sku for b in batches}

