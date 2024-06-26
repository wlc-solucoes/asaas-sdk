from asaas.exceptions import raise_for_status
from asaas.customer import Customer
from asaas.utils import remove_none_and_empty_values

import requests
from requests import Response

from typing import Optional


class Asaas:
    """SDK for Asaas API"""

    def __init__(
        self,
        api_key: str,
        production: bool = False
    ):
        print(api_key)
        self.base_url = 'https://www.asaas.com/api/v3' if production else 'https://sandbox.asaas.com/api/v3'
        self.headers = {
            'access_token': api_key
        }

        self.customers = Costumers(self)

    def get(
        self,
        endpoint: str,
        params: Optional[dict] = None
    ) -> Response:
        """Make a GET request to Asaas API"""

        response = requests.get(
            f'{self.base_url}/{endpoint}',
            headers=self.headers,
            params=params
        )
        raise_for_status(response)

        return response

    def post(
        self,
        endpoint: str,
        data: dict
    ) -> Response:
        """Make a POST request to Asaas API"""

        response = requests.post(
            f'{self.base_url}/{endpoint}',
            headers=self.headers,
            json=data
        )
        raise_for_status(response)

        return response

    def put(
        self,
        endpoint: str,
        data: dict
    ) -> Response:
        """Make a PUT request to Asaas API"""

        response = requests.put(
            f'{self.base_url}/{endpoint}',
            headers=self.headers,
            json=data
        )
        raise_for_status(response)

        return response

    def delete(
        self,
        endpoint: str
    ) -> Response:
        """Make a DELETE request to Asaas API"""

        response = requests.delete(
            f'{self.base_url}/{endpoint}',
            headers=self.headers
        )
        raise_for_status(response)

        return response
