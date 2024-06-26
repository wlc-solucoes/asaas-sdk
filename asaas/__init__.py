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
            f'{self.base_url}/{endpoint}/',
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
            f'{self.base_url}/{endpoint}/',
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
            f'{self.base_url}/{endpoint}/',
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
            f'{self.base_url}/{endpoint}/',
            headers=self.headers
        )
        raise_for_status(response)

        return response


class Costumers:
    """Class to manage customers in Asaas API"""

    def __init__(self, asaas: Asaas):
        self.asaas = asaas
        self.endpoint = 'customers'

    def retrieve(
        self,
        customer_id: str
    ) -> Customer:
        """Retrieve a customer by ID"""

        response = self.asaas.get(f'{self.endpoint}/{customer_id}')

        return Customer(**response.json())

    def create(
        self,
        name: str,
        cpfCnpj: str,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        mobilePhone: Optional[str] = None,
        address: Optional[str] = None,
        addressNumber: Optional[str] = None,
        complement: Optional[str] = None,
        province: Optional[str] = None,
        postalCode: Optional[str] = None,
        externalReference: Optional[str] = None,
        notificationDisabled: Optional[bool] = None,
        additionalEmails: Optional[str] = None,
        municipalInscription: Optional[str] = None,
        stateInscription: Optional[str] = None,
        observations: Optional[str] = None,
        groupName: Optional[str] = None,
        company: Optional[str] = None
    ) -> Customer:
        """Create a new customer"""

        data = remove_none_and_empty_values(
            {
                'name': name,
                'cpfCnpj': cpfCnpj,
                'email': email,
                'phone': phone,
                'mobilePhone': mobilePhone,
                'address': address,
                'addressNumber': addressNumber,
                'complement': complement,
                'province': province,
                'postalCode': postalCode,
                'externalReference': externalReference,
                'notificationDisabled': notificationDisabled,
                'additionalEmails': additionalEmails,
                'municipalInscription': municipalInscription,
                'stateInscription': stateInscription,
                'observations': observations,
                'groupName': groupName,
                'company': company
            }
        )

        response = self.asaas.post(f'{self.endpoint}', data)

        return Customer(**response.json())

    def list(
        self,
        name: Optional[str] = None,
        email: Optional[str] = None,
        cpfCnpj: Optional[str] = None,
        groupName: Optional[str] = None,
        externalReference: Optional[str] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None
    ) -> list[Customer]:
        """List customers"""

        params = remove_none_and_empty_values(
            {
                'offset': offset,
                'limit': limit,
                'name': name,
                'email': email,
                'cpfCnpj': cpfCnpj,
                'groupName': groupName,
                'externalReference': externalReference
            }
        )

        response = self.asaas.get(self.endpoint, params)

        return [Customer(**customer) for customer in response.json()['data']]

    def update(
        self,
        customer_id: str,
        name: str,
        cpfCnpj: str,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        mobilePhone: Optional[str] = None,
        address: Optional[str] = None,
        addressNumber: Optional[str] = None,
        complement: Optional[str] = None,
        province: Optional[str] = None,
        postalCode: Optional[str] = None,
        externalReference: Optional[str] = None,
        notificationDisabled: Optional[bool] = None,
        additionalEmails: Optional[str] = None,
        municipalInscription: Optional[str] = None,
        stateInscription: Optional[str] = None,
        observations: Optional[str] = None,
        groupName: Optional[str] = None,
        company: Optional[str] = None
    ) -> Customer:
        """Update a customer by ID"""

        data = remove_none_and_empty_values(
            {
                'name': name,
                'cpfCnpj': cpfCnpj,
                'email': email,
                'phone': phone,
                'mobilePhone': mobilePhone,
                'address': address,
                'addressNumber': addressNumber,
                'complement': complement,
                'province': province,
                'postalCode': postalCode,
                'externalReference': externalReference,
                'notificationDisabled': notificationDisabled,
                'additionalEmails': additionalEmails,
                'municipalInscription': municipalInscription,
                'stateInscription': stateInscription,
                'observations': observations,
                'groupName': groupName,
                'company': company
            }
        )

        response = self.asaas.put(
            f'{self.endpoint}/{customer_id}',
            data
        )

        return Customer(**response.json())

    def delete(
        self,
        customer_id: str
    ) -> None:
        """Delete a customer by ID"""

        self.asaas.delete(f'customers/{customer_id}')

    def restore(
        self,
        customer_id: str
    ) -> Customer:
        """Restore a customer by ID"""

        response = self.asaas.post(f'{self.endpoint}/{customer_id}/restore')

        return Customer(**response.json())
