from flask import current_app as app, request
from sqlalchemy.exc import InvalidRequestError, ProgrammingError

from ..utils import create_response, tuplify_query_result
from ..models import Product, db, get_product
from ..messages import ProductMessages
from ..decorators import (
    check_body_supplied, check_product_exists, check_valid_product_body
)


@app.route("/")
def index():
    return create_response(200, "Api is doing well, thanks for asking")


@app.route("/products", methods=('GET',))
def load_products():
    products = tuplify_query_result(Product.query.all())
    return create_response(200, "", products)


@app.route("/product", methods=('PUT',))
@check_body_supplied
@check_valid_product_body(("id",))
def create_product():
    product = Product(**request.get_json())
    try:
        db.session.add(product)
        db.session.commit()
        # register product in Offer service
        # the refresher job will ad offers to new created
        app.config["offers_service"].register_product(product)
    except (InvalidRequestError, ProgrammingError) as ex:
        return create_response(500, str(ex))

    return create_response(200, ProductMessages.created, data=product.dump_dict())


@app.route("/product/<pid>", methods=('GET',))
@check_product_exists
def load_product(pid: int):
    return create_response(200, "", get_product(pid).dump_dict())


@app.route("/product/<pid>", methods=('POST',))
@check_body_supplied
@check_valid_product_body(("id",))
def edit_product(pid: int):
    try:
        db.session.query(Product).filter(Product.id == pid).update(request.get_json())
        db.session.commit()
    except (InvalidRequestError, ProgrammingError) as ex:
        return create_response(500, str(ex))

    return create_response(200, ProductMessages.updated)


@app.route("/product/<pid>", methods=('DELETE',))
@check_product_exists
def delete_product(pid: int):
    try:
        db.session.query(Product).filter(Product.id == pid).delete()
        db.session.commit()
    except (InvalidRequestError, ProgrammingError) as ex:
        return create_response(500, str(ex))

    return create_response(200, ProductMessages.removed)
