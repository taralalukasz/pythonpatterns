from flask import Flask, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from service_layer.services import allocate, deallocate
from domain.model import OrderLine, OutOfStock, InvalidSku

import config
import adapters.orm
import adapters.repository



adapters.orm.start_mappers()
get_session = sessionmaker(bind=create_engine(config.get_postgres_uri()))
app = Flask(__name__)


@app.route("/allocate", methods=["POST"])
def allocate_endpoint():
    session = get_session()
    batches = adapters.repository.SqlAlchemyRepository(session).list()
    line = OrderLine(
        request.json["orderid"], request.json["sku"], request.json["qty"],
    )

    try:
        batchref = allocate(line, batches)
    except OutOfStock as e:
        return {"message": str(e)}, 400
    
    return {"batchref": batchref}, 201



@app.route("/deallocate", methods=["POST"])
def deallocate_endpoint():
    session = get_session()
    batches = adapters.repository.SqlAlchemyRepository(session).list()
    line = OrderLine(
        request.json["orderid"], request.json["sku"], request.json["qty"],
    )

    try:
        batchref = deallocate(line, batches)
    except InvalidSku as e:
        return {"message": str(e)}, 400
    
    return {"batchref": batchref}, 201