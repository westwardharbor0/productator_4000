from flask import current_app as app

from ..utils import create_response, tuplify_query_result
from ..models import Offer
from ..decorators import check_product_exists


@app.route("/offers/<pid>", methods=('GET',))
@check_product_exists
def load_offers(pid: int):
    offers = tuplify_query_result(Offer.query.filter(Offer.product_id == pid).all())
    return create_response(200, "", offers)
