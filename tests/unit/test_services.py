import service_layer.services as services
import domain.model as model
from adapters.repository import FakeRepository, FakeSession

import pytest

def test_returns_allocation():
    batch = model.Batch("ref", "COMPLICATED-LAMP", 20, None)
    line = model.OrderLine("orderid", "COMPLICATED-LAMP", 10)
    repo  = FakeRepository([batch])
    session = FakeSession()
    batchref = services.allocate(line, repo, session)

    assert batchref == "ref"


def test_returns_deallocation():
    batch = model.Batch("ref", "COMPLICATED-LAMP", 20, None)
    line = model.OrderLine("orderid", "COMPLICATED-LAMP", 10)
    batch.allocate(line)
    repo  = FakeRepository([batch])
    session = FakeSession()
    batchref = services.deallocate(line, repo, session)

    assert batchref == "ref"

def test_error_for_invalid_sku_try_to_deallocate_not_allocated_item():
    batch = model.Batch("ref", "COMPLICATED-LAMP", 20, None)
    line = model.OrderLine("orderid", "COMPLICATED-LAMP", 10)

    batch.deallocate(line)
    repo  = FakeRepository([batch])
    session = FakeSession()
    
    with pytest.raises(model.InvalidSku, match="Cannot deallocate sku COMPLICATED-LAMP"):
        services.deallocate(line, repo, session)


def test_error_for_invalid_sku():
    batch = model.Batch("ref", "COMPLICATED-LAMP", 20, None)
    line = model.OrderLine("orderid", "INVALID-SKU", 10)
    repo  = FakeRepository([batch])
    session = FakeSession()
    
    with pytest.raises(model.InvalidSku, match="Invalid sku INVALID-SKU"):
        services.allocate(line, repo, session)

def test_commits():
    line = model.OrderLine("o1", "OMINOUS-MIRROR", 10)
    batch = model.Batch("b1", "OMINOUS-MIRROR", 100, eta=None)
    repo = FakeRepository([batch])
    session = FakeSession()

    services.allocate(line, repo, session)
    assert session.committed is True