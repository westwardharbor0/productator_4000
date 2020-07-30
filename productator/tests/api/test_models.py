from ...src.models import Product


def test_model_dict_dump():
    # Check that dump to dict contains all fields
    test_dict = {
        "id": 1,
        "name": "test",
        "description": "test"
    }
    product = Product(**test_dict)
    assert product.dump_dict() == test_dict


def test_model_fields_list():
    # Check that the fields listing is working right
    assert len(Product.fields()) == 3
    assert len(Product.fields(exclude=("id",))) == 2
    assert len(Product.fields(exclude=("id", "name"))) == 1
