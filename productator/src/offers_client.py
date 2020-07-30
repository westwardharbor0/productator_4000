from requests import post, get, Response, HTTPError
from json import dumps


# endpoints supported by the offers service
URLS = {
    "auth": "/auth",
    "register": "/products/register",
    "offers": "/products/{}/offers"
}


class OffersClient(object):
    """
    Basic client for offers service interaction
    """
    def __init__(self, base: str, token: str = ""):
        """
        Constructor
        :param base: url base for future requests
        :param token: optional token to access service
        """
        self._base: str = base
        self._token: str = token
        if not token:
            # if no token provided we generate him
            self._authenticate()

    @staticmethod
    def _check_response(response: Response):
        """
        Checks response status code from api
        :param response: response from request
        """
        if response.status_code not in (200, 201):
            raise HTTPError(response=response)

    def _post(self, url: str, data: dict = None) -> (dict, list):
        """
        Creates a post request to the service
        :param url: path to the desired endpoint in service
        :param data: optional data to send with post
        :return: dict with response data
        """
        response = post(self._base + url, data=dumps(data), headers=self._headers())
        self._check_response(response)
        return response.json()

    def _get(self, url: str, params: dict = None, headers: dict = None) -> (dict, list):
        """
        Creates a get request to the service
        :param url: path to the desired endpoint in service
        :param params: optional params to put in url
        :param headers: optional headers dict to send
        :return: dict with response data
        """
        response = get(
            self._base + url,
            params=params,
            headers=headers or self._headers()
        )
        self._check_response(response)
        return response.json()

    def _authenticate(self):
        self._token = self._post(URLS["auth"])["access_token"]

    def _headers(self) -> dict:
        """
        Generates general headers containing access token
        :return: dict with headers
        """
        return {
            'Content-Type': 'application/json',
            'Bearer': self._token
        }

    def register_product(self, product) -> dict:
        """
        Registers new product in the offers service
        :param product: filled product model to save
        :return: dict with id of created product
        """
        return self._post(URLS["register"], data=product.dump_dict())

    def load_offers(self, product_id: int) -> list:
        """
        Loads offers for a product from the offers service
        :param product_id: id of a created product
        :return: list of offers (dicts) for a product
        """
        return self._get(URLS["offers"].format(product_id))

