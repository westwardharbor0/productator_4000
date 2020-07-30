from ...refresher import Refresher

# DB state with offers
DB_DATA = {
    1: {
        "id": 1,
        "product_id": 1,
        "items_in_stock": 1,
        "price": 1
    },
    2: {
        "id": 2,
        "product_id": 1,
        "items_in_stock": 1,
        "price": 1
    },
    4: {
        "id": 2,
        "product_id": 1,
        "items_in_stock": 1,
        "price": 1
    }
}
# APi state with offers
API_DATA = {
    1: {
        "id": 1,
        "product_id": 1,
        "items_in_stock": 2,
        "price": 1
    },
    3: {
        "id": 3,
        "product_id": 1,
        "items_in_stock": 1,
        "price": 1
    },
    4: {
        "id": 2,
        "product_id": 1,
        "items_in_stock": 1,
        "price": 1
    }
}


def test_sorting():
    # test that offers from api are being recognised right
    create, update, delete = Refresher.compare_offers(DB_DATA, API_DATA)
    assert len(create) == 1
    assert len(update) == 1
    assert len(delete) == 1
