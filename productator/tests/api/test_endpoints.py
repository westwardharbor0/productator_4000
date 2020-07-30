from pytest import fixture
from os import environ
from json import dumps
from flask import Response

from ...src import make_app


environ.setdefault("PRODUCTATOR_CONFIG", "confs/tests.conf.json")

# default headers for communication with API
HEADERS = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}


@fixture(scope='module')
def test_client():
    # create a test client to access API
    flask_app = make_app()
    testing_client = flask_app.test_client()
    ctx = flask_app.app_context()
    ctx.push()
    yield testing_client
    ctx.pop()

# ------------------------------------------------------ #
#                   ENDPOINT TEST                        #
# ------------------------------------------------------ #


def test_index(test_client):
    # test that api is running
    res = test_client.get("/")
    assert res.status_code == 200


def test_products_load(test_client):
    # test loading all products (can be empty)
    res = test_client.get("/products")
    assert res.status_code == 200


def test_product_create(test_client):
    # test product can be created
    def create_product(d: dict) -> Response:
        """
        Helper for product creating
        :param d: data for product creation
        :return: response from API
        """
        return test_client.put("/product", data=dumps(d), headers=HEADERS)

    # test regular creating of product
    res = create_product({"id":1, "name": "pytest-product", "description": "pytest-product-desc"})
    assert res.status_code == 200
    # test misspelled field detected
    res = create_product({"_name": "pytest-product", "description": "pytest-product-desc"})
    assert res.status_code == 500
    # test extra field detected
    res = create_product({"pname": "", "name": "pytest-product", "description": "pytest-product-desc"})
    assert res.status_code == 500


def test_product_load(test_client):
    # test that we can load a product
    res = test_client.get("/product/1", headers=HEADERS)
    assert res.status_code == 200
    dict_res = res.json.get("result")
    assert "id" in dict_res
    assert "name" in dict_res
    assert "description" in dict_res


def test_product_update(test_client):
    # Test that product can be updated
    update_date = {"name": "pytest-product-updated", "description": "pytest-product-desc"}
    res = test_client.post("/product/1", data=dumps(update_date), headers=HEADERS)
    assert res.status_code == 200
    res = test_client.get("/product/1", headers=HEADERS)
    assert res.status_code == 200
    # check name really updated
    assert res.json.get("result")["name"] == update_date["name"]


def test_offers_load(test_client):
    # Test that product offers can be loaded
    res = test_client.get("/offers/1", headers=HEADERS)
    assert res.status_code == 200


def test_product_delete(test_client):
    # Test that product can be removed
    res = test_client.delete("/product/1", headers=HEADERS)
    assert res.status_code == 200
    res = test_client.get("/product/1", headers=HEADERS)
    assert res.status_code == 404
