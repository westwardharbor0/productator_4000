from sqlalchemy.ext.baked import Result
from json import load
from os import environ


def create_response(code, message, data=()) -> (dict, int):
    """
    Helper to create response
    :param code: http status code
    :param message: additional text message to extend code meaning
    :param data: result data of the request
    :return:
    """
    return {
        "code": code,
        "message": message,
        "result": data
    }, code


def tuplify_query_result(result: Result):
    """
    Convert sqlalchemy result to tuple
    :param result: sqlalchemy result
    :return: tuple of result
    """
    return tuple(i.dump_dict() for i in result)


def generate_config_dict(file_path: str) -> dict:
    """
    Loads config file into a dict
    :param file_path: path to config file
    :return: dict of configuration
    """
    with open(file_path) as conf:
        config_dict = load(conf)
    return config_dict


def generate_db_connection_string(storage_dict: dict) -> str:
    """
    Creates a connection string to mysql DB for engine_create()
    :param storage_dict: dict containing keys / values for DB connect
    :return: string for db connection
    """
    return "mysql+pymysql://{user}:{password}@{host}/{database}?charset=utf8mb4".format(
        user=storage_dict["database"]["user"],
        password=storage_dict["database"]["password"],
        host=environ.get("DATABASE_HOST") or storage_dict["database"]["host"],
        database=storage_dict["database"]["db"]
    )
