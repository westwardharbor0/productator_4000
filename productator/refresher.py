from pymysql import connect, Connection
from pymysql.cursors import Cursor
from os import environ
from logging import info, basicConfig, INFO
from time import sleep

from .src.models import Product, Offer
from .src.offers_client import OffersClient
from .src.utils import generate_config_dict


class Refresher(object):
    """
    Refresher class to contain all the logic
    It's a class mainly because of tests -__-
    """
    def __init__(self, config_path: str = None, db_host: str = None, delay: int = None):
        self.config_path = config_path
        self.db_host = db_host
        self.delay = delay

    def init_refresher(self) -> (OffersClient, Connection):
        """
        Prepares all the connections for refresher
        :return: initialized offers client and db connection
        """
        basicConfig(level=INFO)
        config = generate_config_dict(self.config_path)
        # add support for ENV var override of host of database
        if self.db_host:
            config["database"]["host"] = self.db_host

        conn = connect(**config["database"])
        client = OffersClient(config["offers_address"], config["offers_token"])

        return client, conn

    @staticmethod
    def get_products(cursor: Cursor) -> tuple:
        """
        Returns all stored product ids in DB
        :param cursor: connection cursor to DB
        :return: all product ids
        """
        cursor.execute("SELECT `id` FROM `{}` ".format(Product.__tablename__))
        return cursor.fetchall()

    @staticmethod
    def get_product_offers(cursor: Cursor, pid: int) -> tuple:
        """
        Returns all offers for a product
        :param cursor: connection cursor to DB
        :param pid: product id
        :return: all offers for a product formatted to dict with columns names
        """
        fields = Offer.fields()
        cursor.execute("SELECT {} FROM `{}` WHERE `product_id` = {}".format(",".join(fields), Offer.__tablename__, pid))
        return tuple(dict(zip(fields, row)) for row in cursor.fetchall())

    @staticmethod
    def index_offers(offers: (list, tuple)) -> dict:
        """
        Creates a simple dict of offers so it can be handled easier
        :param offers: offers to be converted to dict
        :return: dict of offers with offer id as key
        """
        return {offer["id"]: offer for offer in offers}

    @staticmethod
    def compare_offers(db_offers: dict, api_offers: dict) -> (list, list, list):
        """
        Compares two offer dicts for changes
        :param db_offers: offers loaded from db in dict format
        :param api_offers: offers loaded from api in dict format
        :return: changes that need to be done grouped by action
        """
        create, update, delete = [], [], []
        for api_offer_id in api_offers:
            api_offer = api_offers.get(api_offer_id)
            db_offer = db_offers.get(api_offer_id)
            # if the offer is not stored yet, we create it
            if not db_offer:
                create.append(api_offer)
                continue
            # if there are some changes in found offer
            if db_offer != api_offer:
                update.append(api_offer)
        # if offer is in DB but not in api it will be removed
        for db_offer_id in db_offers:
            if not api_offers.get(db_offer_id):
                delete.append(db_offer_id)

        return create, update, delete

    @staticmethod
    def create_offers(cursor: Cursor, product_id: int, offers: list):
        """
        Creates the new found offers from api
        :param cursor: connection cursor to DB
        :param product_id: product id from DB
        :param offers: list of offers that will be created
        """
        o_fields = Offer.fields()
        values = []
        for offer in offers:
            offer["product_id"] = product_id
            values.append(tuple(int(offer[key]) for key in o_fields))
        placeholder = ["%s" for _ in o_fields]
        cursor.executemany(
            "INSERT INTO `{}` ({}) VALUES ({})".format(
                Offer.__tablename__, ", ".join(o_fields), ", ".join(placeholder)
            ), values
        )

    @staticmethod
    def update_offers(cursor: Cursor, product_id: int, offers: list):
        """
        Creates query to update data in DB
        :param cursor: connection cursor to DB
        :param product_id: product id
        :param offers: list of offers that will be updated
        """
        values = []
        for offer in offers:
            sets = []
            for key in offer:
                sets.append(offer[key])
            values.append(sets)
        # because product_id is specific for DB it needs to be removed
        placeholder = ["{} = %s".format(field) for field in Offer.fields(("product_id",))]
        query = """
        UPDATE `{}` SET {} WHERE id = {}
        """.format(Offer.__tablename__,  ", ".join(placeholder), product_id).strip()
        cursor.executemany(query, values)

    @staticmethod
    def delete_offers(cursor: Cursor, product_id: int, offers: list):
        """
        Creates query to delete obsolete data in DB
        :param cursor: connection cursor to DB
        :param product_id: product id
        :param offers: list of offers that will be updated
        """
        cursor.execute(
            """
                DELETE FROM {} WHERE `id` IN ({}) AND `product_id` = {}
            """.format(
                Offer.__tablename__, ", ".join([str(offer) for offer in offers]), product_id
            )
        )

    def refresh(self):
        """
        Main method for running refresher
        """
        # create connection to API and DB
        offer_client, connection = self.init_refresher()
        while True:
            # run in a endless loop to refresh
            info("--- Refreshing the offers ---")
            with connection.cursor() as cursor:
                # load all the products we have for refresh
                for product in self.get_products(cursor):
                    pid = product[0]
                    info("__" * 15)
                    info("Processing product id:{}".format(pid))
                    # load possible updated offers for product
                    api_offers = self.index_offers(offer_client.load_offers(pid))
                    db_offers = self.index_offers(self.get_product_offers(cursor, pid))

                    create, update, delete = self.compare_offers(db_offers, api_offers)
                    if create:
                        info("Creating {} new offers of product".format(len(create)))
                        self.create_offers(cursor, pid, create)

                    if update:
                        info("Updating {} offers of product".format(len(update)))
                        self.update_offers(cursor, pid, update)

                    if delete:
                        info("Deleting {} old offers of product".format(len(delete)))
                        self.delete_offers(cursor, pid, delete)
            # commit all changes
            connection.commit()
            sleep(self.delay)


if __name__ == '__main__':
    refresher = Refresher(
        config_path=environ.get("REFRESHER_CONFIG"),
        db_host=environ.get("DATABASE_HOST"),
        delay=int(environ.get("REFRESHER_PERIOD", 30))
    )
    refresher.refresh()


