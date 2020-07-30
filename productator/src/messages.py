
class GeneralMessages:
    """
    General messages used in API
    """
    starting_api = "Starting Productator API"
    initialized_db = "Database access initialized"
    initialized_offers = "Offers service initialized"
    initialized_routes = "API endpoints initialized"
    initialized_config = "Config file loaded"
    missing_params = "No parameters supplied, nothing to do"
    incomplete_params = "Some parameters are missing to complete task"
    garbage_params = "To much parameters send, exclude them"


class ProductMessages:
    """
    Product specific messages used in API
    """
    updated = "Product was updated"
    created = "Product was created"
    removed = "Product was removed"
    not_found = "Product with id: {} could not be found"
