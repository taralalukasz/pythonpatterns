from flask import Flask, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from service_layer.services import allocate
from domain.model import OrderLine, OutOfStock, InvalidSku

import config
import adapters.orm
import adapters.repository



adapters.orm.start_mappers()
get_session = sessionmaker(bind=create_engine(config.get_postgres_uri()))
app = Flask(__name__)



def is_valid_sku(sku, batches):
    return sku in {b.sku for b in batches}


@app.route("/allocate", methods=["POST"])
def allocate_endpoint():
    session = get_session()
    batches = adapters.repository.SqlAlchemyRepository(session).list()
    line = OrderLine(
        request.json["orderid"], request.json["sku"], request.json["qty"],
    )

    if not is_valid_sku(line.sku, batches):
        return {"message": f"Invalid sku {line.sku}"}, 400

    try:
        batchref = allocate(line, batches)
    except OutOfStock as e:
        return {"message": str(e)}, 400

    session.commit()
    return {"batchref": batchref}, 201