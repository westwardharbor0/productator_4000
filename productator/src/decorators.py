from flask import request
from functools import wraps

from .models import get_product, Product
from .utils import create_response
from .messages import GeneralMessages, ProductMessages


def check_body_supplied(f):
    """
    Decorator for checking in any body was send
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        if not request.get_json():
            return create_response(200, GeneralMessages.missing_params)
        return f(*args, **kwargs)
    return decorated


def check_product_exists(f):
    """
    Decorator for checking if Product exists in our DB
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        pid = kwargs.get("pid")
        if not get_product(pid):
            return create_response(404, ProductMessages.not_found.format(pid))
        return f(*args, **kwargs)
    return decorated


def check_valid_product_body(exclude=()):
    """
    Decorator to check if all needed fields are in the request body
    """
    def wrapper(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            in_req = tuple(set(request.get_json().keys()) - set(Product().fields()) - set(exclude))
            in_model = tuple(set(Product().fields()) - set(request.get_json().keys()) - set(exclude))
            if in_req:
                return create_response(500, GeneralMessages.garbage_params, {"fields": in_req})
            if in_model:
                return create_response(500, GeneralMessages.incomplete_params, {"fields": in_model})
            return f(*args, **kwargs)
        return decorated
    return wrapper
