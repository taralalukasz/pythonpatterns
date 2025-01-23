import pytest
import uuid
import requests


import config

# add_stock must be a helper function, which populates database when test starts
@pytest.mark.usefixtures("restart_api")
def test_api_returns_allocation(add_stock):
    sku, othersku = random_sku(), random_sku("other")  
    earlybatch = random_batchref(1)
    laterbatch = random_batchref(2)
    otherbatch = random_batchref(3)
    add_stock(  #(2)
        [
            (laterbatch, sku, 100, "2011-01-02"),
            (earlybatch, sku, 100, "2011-01-01"),
            (otherbatch, othersku, 100, None),
        ]
    )
    data = {"orderid": random_orderid(), "sku": sku, "qty": 3}
    url = config.get_api_url()  #(3)

    r = requests.post(f"{url}/allocate", json=data)

    assert r.status_code == 201
    assert r.json()["batchref"] == earlybatch

@pytest.mark.usefixtures("restart_api")
def test_400_message_for_out_of_stock(add_stock):
    sku, batchref, large_orderid = random_sku(), random_batchref(), random_orderid()
    add_stock(  
        [
            (batchref, sku, 10, "2011-01-02"),
        ]
    )
    data = {"orderid": large_orderid, "sku": sku, "qty" : 20}
    url = config.get_api_url()
    r = requests.post(f"{url}/allocate", json=data)

    assert r.status_code == 400
    assert r.json["message"] == f"Out of stock for {sku}"

@pytest.mark.usefixtures("restart_api")
def test_400_message_for_invalid_sku(add_stock):
    sku, unknown_sku, orderid = random_sku(), random_sku("other"), random_orderid()
    batchref = random_batchref()
    add_stock( 
        [
            (batchref, sku, 10, "2011-01-02"),
        ]
    )
    data = {"orderid":orderid, "sku":unknown_sku, "qty":2}
    url = config.get_api_url()
    r = requests.post(f"{url}/allocate", json=data)
    assert r.status_code == 400
    assert r.json["message"] == f"Invalid sku {unknown_sku}"



def random_suffix():
    return uuid.uuid4().hex[:6]


def random_sku(name=""):
    return f"sku-{name}-{random_suffix()}"


def random_batchref(name=""):
    return f"batch-{name}-{random_suffix()}"


def random_orderid(name=""):
    return f"order-{name}-{random_suffix()}"
