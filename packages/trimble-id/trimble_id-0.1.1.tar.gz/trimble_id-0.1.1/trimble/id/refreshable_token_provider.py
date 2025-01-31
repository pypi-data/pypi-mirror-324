import json

from .http_client import HttpClient
from ._constants import PACKAGE_NAME
from ._version import VERSION

class RefreshableTokenProvider:
    """
    A refreshable token provider based on the OAuth refresh token grant type
    """
    def __init__(self, endpoint_provider, client_id, client_secret, token, product_name = None):
        """
        Initialize RefreshableTokenProvider class

        :param endpoint_provider: An endpoint provider that provides the URL for the Trimble Identity token endpoint
        :param client_id: The consumer key for the calling application
        :param client_secret: The consumer secret for the calling application
        :param token: The initial access token issued for the authenticated user
        :param product_name: Product name of the calling application
        """
        self._endpointProvider = endpoint_provider
        self._consumerKey = client_id
        self._consumerSecret = client_secret
        self._token = token

        self._version = VERSION
        self._productName = product_name

    async def retrieve_token(self):
        """
        Retrieves an access token for the application using refresh grant type

        :return: The access token for the given application
        """
        tokenEndpoint = await self._endpointProvider.retrieve_token_endpoint()
        client = HttpClient('', {})
        result = await client.post(
            tokenEndpoint, 
            'grant_type=refresh_token&client_id=' + self._consumerKey + '&client_secret=' + self._consumerSecret, 
            { 'content-type': 'application/x-www-form-urlencoded', 'accept': 'application/json', 'user-agent': f"{PACKAGE_NAME}/{self._version} python-sdk {self._productName}" }
        )
        jsonResult = json.loads(result)
        return jsonResult['access_token']