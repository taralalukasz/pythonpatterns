import service_layer.services as services
import domain.model as model
from adapters.repository import FakeRepository, FakeSession
from datetime import date, timedelta

import pytest

tomorrow = date.today() + timedelta(days=1)

def test_returns_allocation():
    repo, session = FakeRepository(), FakeSession()
    services.add_batch("ref", "COMPLICATED-LAMP", 20, None, repo, session)
    batchref = services.allocate("orderid", "COMPLICATED-LAMP", 10, repo, session)

    assert batchref == "ref"


def test_returns_deallocation():
    repo, session = FakeRepository(), FakeSession()
    line = model.OrderLine("orderid", "COMPLICATED-LAMP", 10)
    services.add_batch("ref", "COMPLICATED-LAMP", 20, None, repo, session)
    services.allocate("orderid", "COMPLICATED-LAMP", 10, repo, session)

    batchref = services.deallocate("orderid", "COMPLICATED-LAMP", 10, repo, session)

    assert batchref == "ref"

def test_error_for_invalid_sku_try_to_deallocate_not_allocated_item():
    repo, session = FakeRepository(), FakeSession()
    services.add_batch("ref", "COMPLICATED-LAMP", 20, None, repo, session)
    
    with pytest.raises(model.InvalidSku, match="Cannot deallocate sku COMPLICATED-LAMP"):
        services.deallocate("orderid", "COMPLICATED-LAMP", 10, repo, session)


def test_error_for_invalid_sku():
    repo, session = FakeRepository(), FakeSession()
    services.add_batch("ref", "COMPLICATED-LAMP", 20, None, repo, session)
    
    with pytest.raises(model.InvalidSku, match="Invalid sku INVALID-SKU"):
        services.allocate("orderid", "INVALID-SKU", 10, repo, session)

def test_commits():
    repo, session = FakeRepository(), FakeSession()
    services.add_batch("b1", "OMINOUS-MIRROR", 100, None, repo, session)
    services.allocate("o1", "OMINOUS-MIRROR", 10, repo, session)
    assert session.committed is True

def test_prefers_warehouse_batches_to_shipments():
    repo, session = FakeRepository(), FakeSession()
    services.add_batch("b1", "OMINOUS-MIRROR", 100, None, repo, session)
    services.add_batch("b2", "NOTHER-SKU", 100, None, repo, session)

    batchref = services.allocate("o1", "OMINOUS-MIRROR", 10, repo, session)
    
    assert batchref == "b1"
    
