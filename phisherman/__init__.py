import platform
import requests
import validators

from typing import Union
from requests import Response

from phisherman.errors import PhishermanAPIException, PhishermanClientException


class Phisherman:

    def __init__(self, token: str = None) -> None:
        """
        The Phisherman class constructor

        Args:
            token (str): The Phisherman API token

        Raises:
            PhishermanClientException: If no token was passed to the constructor
        """

        if not token:
            raise PhishermanClientException('Did you pass an API Key?')

        self.base = "https://api.phisherman.gg/v2"
        self.__version__ = '0.0.1'

        revision = platform.python_revision()
        impl = platform.python_implementation()
        version = platform.python_version()
        machine = platform.uname()

        self.headers = {
            'User-Agent': f'Phisherman/{self.__version__} (wrapper) ({impl}/{version}-{revision}; {machine.system}/{machine.version}; {machine.machine}) (+https://github.com/IlluminatiFish/Phisherman)',
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

    def _execute_request(self, method: str, endpoint: str, data: dict = None) -> Response:
        """
        An internal function to execute requests based on the specified arguments

        Args:
            method (str): The HTTP method used in the request
            endpoint (str): The endpoint the request is being made to
            data (dict): The JSON data being sent

        Returns:
            A Response object from the requests library
        """

        if not data:
            response = requests.request(method, f'{self.base}{endpoint}', headers = self.headers, data = data)
        else:
            response = requests.request(method, f'{self.base}{endpoint}', headers = self.headers)

        return response

    def check_domain(self, domain: str) -> Union[dict, None]:
        """
        Lookups the specified domain

        Args:
            domain (str): The domain to get the information from

        Returns:
            A JSON response with the phishing-specific information about the `domain`

        Raises:
            PhishermanClientException: Raised when the API client reaches an error during validation
            PhishermanAPIException: Raised when the API directly returns an error from the request
        """

        if domain is None:
            raise PhishermanClientException('No domain supplied')

        if validators.domain(domain) is False:
            raise PhishermanClientException('Invalid domain supplied')

        response = self._execute_request('GET', f'/domains/check/{domain}')
        json_response = response.json()

        success = json_response.get('success', True)

        if success is False:
            message = json_response.get('message')
            raise PhishermanAPIException(f'{message}')

        return json_response

    def get_domain_info(self, domain: str) -> Union[dict, None]:
        """
        Gets the information of a specified domain

        Args:
            domain (str): The domain to get the information from

        Returns:
            A JSON response with the information about the `domain`

        Raises:
            PhishermanClientException: Raised when the API client reaches an error during validation
            PhishermanAPIException: Raised when the API directly returns an error from the request
        """

        if domain is None:
            raise PhishermanClientException('No domain supplied')

        if validators.domain(domain) is False:
            raise PhishermanClientException('Invalid domain supplied')

        response = self._execute_request('GET', f'/domains/info/{domain}')
        json_response = response.json()

        success = json_response.get('success', True)

        if success is False:
            message = json_response.get('message')
            raise PhishermanAPIException(f'{message}')

        return json_response.get(domain)

    def report_caught_phish(self, domain: str = None, guild: int = None) -> Union[bool, None]:
        """
        Reports a phish that was caught in a specified guild

        Args:
            domain (str): The domain of the caught phish
            guild (int): The ID of the guild that the phish was caught in

        Returns:
            A boolean indicating whether the report was successful or not

        Raises:
            PhishermanClientException: Raised when the API client reaches an error during validation
            PhishermanAPIException: Raised when the API directly returns an error from the request
        """

        if domain is None:
            raise PhishermanClientException('Supply a domain to report')

        if guild is None:
            raise PhishermanClientException('Supply a guild id to report from')

        if validators.domain(domain) is False:
            raise PhishermanClientException('Invalid domain supplied')

        data = {'guild': guild}
        response = self._execute_request('POST', f'/phish/caught/{domain}', data = data)

        success = response.status_code == 204

        if not success:
            raise PhishermanAPIException('Failed to report caught phish')

        return success

