from sqlalchemy import Column, Integer, String
from . import db


class GeneralModel:
    """
    Helper class to add functionality for dumping models
    """
    def dump_dict(self) -> dict:
        """
        Transform model key / values to a dict
        :return: dict of key / values of model
        """
        ret = {}
        for key in self.fields():
            ret[key] = self.__getattribute__(key)
        return ret

    @classmethod
    def fields(cls, exclude=()) -> list:
        """
        Loads all user defined fields in list
        :param exclude: fields to be excluded from result
        :return: list of user defined fields
        """
        ret = []
        for key in cls.__dict__:
            if key.startswith("_") or key in exclude:
                continue
            ret.append(key)
        return ret


class Product(db.Model, GeneralModel):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)


def get_product(pid: int) -> Product:
    """
    Simple helper to load product to not duplicate code
    :param pid: ID of product in DB
    :return: sqllachemy result of found Product
    """
    return Product.query.filter(Product.id == pid).first()


class Offer(db.Model, GeneralModel):
    __tablename__ = "offers"
    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)
    items_in_stock = Column(Integer,  nullable=False)

