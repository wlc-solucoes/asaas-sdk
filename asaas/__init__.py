from asaas import (
    customer,
    payments,
    subscriptions
)
from asaas.utils import remove_none_and_empty_values
from asaas.exceptions import raise_for_status

import requests

from typing import (
    Optional,
    List
)

from datetime import date


class Asaas:
    """SDK for Asaas API"""

    def __init__(
        self,
        api_key: str,
        production: bool = False
    ):
        self.base_url = 'https://www.asaas.com/api/v3' if production else 'https://sandbox.asaas.com/api/v3'
        self.headers = {
            'access_token': api_key
        }

        self.customers = Costumers(self)
        self.payments = Payments(self)
        self.subscriptions = Subscriptions(self)

    def get(
        self,
        endpoint: str,
        params: Optional[dict] = None
    ) -> requests.Response:
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
    ) -> requests.Response:
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
    ) -> requests.Response:
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
    ) -> requests.Response:
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
    ) -> customer.Customer:
        """Retrieve a customer by ID"""

        response = self.asaas.get(f'{self.endpoint}/{customer_id}')

        return customer.Customer(**response.json())

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
    ) -> customer.Customer:
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

        return customer.Customer(**response.json())

    def list(
        self,
        name: Optional[str] = None,
        email: Optional[str] = None,
        cpfCnpj: Optional[str] = None,
        groupName: Optional[str] = None,
        externalReference: Optional[str] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None
    ) -> List[customer.Customer]:
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

        return [customer.Customer(**customer_dict) for customer_dict in response.json()['data']]

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
    ) -> customer.Customer:
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

        return customer.Customer(**response.json())

    def delete(
        self,
        customer_id: str
    ) -> None:
        """Delete a customer by ID"""

        self.asaas.delete(f'customers/{customer_id}')

    def restore(
        self,
        customer_id: str
    ) -> customer.Customer:
        """Restore a customer by ID"""

        response = self.asaas.post(f'{self.endpoint}/{customer_id}/restore')

        return customer.Customer(**response.json())


class ResponseDataToPayment:
    def response_data_to_payment(
        self,
        data: dict
    ):
        """Convert response data to Payment object"""

        data['discount'] = payments.Discount(
            **data['discount']
        ) if data.get('discount') else None

        data['interest'] = payments.Interest(
            **data['interest']
        ) if data.get('interest') else None

        data['fine'] = payments.Fine(
            **data['fine']) if data.get('fine') else None

        data['split'] = [
            payments.Split(**split) for split in data['split']
        ] if data.get('split') else None

        data['chargeback'] = payments.Chargeback(
            **data['chargeback']
        ) if data.get('chargeback') else None

        data['refunds'] = [
            payments.Refund(**refund) for refund in data['refunds']
        ] if data.get('refunds') else None

        return payments.Payment(**data)


class Payments(ResponseDataToPayment):
    """Class to manage payments in Asaas API"""

    def __init__(self, asaas: Asaas):
        self.asaas = asaas
        self.endpoint = 'payments'

    def retrieve(
        self,
        payment_id: str
    ) -> payments.Payment:
        """Retrieve a payment by ID"""

        response = self.asaas.get(f'{self.endpoint}/{payment_id}')

        return self.response_data_to_payment(response.json())

    def create(
        self,
        customer: str,
        value: float,
        dueDate: date,
        billingType: payments.BillingType = payments.BillingType.UNDEFINED,
        description: Optional[str] = None,
        daysAfterDueDateToRegistrationCancellation: Optional[int] = None,
        externalReference: Optional[str] = None,
        installmentCount: Optional[int] = None,
        totalValue: Optional[float] = None,
        installmentValue: Optional[float] = None,
        discount: Optional[payments.Discount] = None,
        interest: Optional[payments.Interest] = None,
        fine: Optional[payments.Fine] = None,
        postalService: Optional[bool] = None,
        split: Optional[List[payments.Split]] = None,
        callback: Optional[payments.Callback] = None
    ) -> payments.Payment:
        discount = discount.to_dict() if discount else None
        interest = interest.to_dict() if interest else None
        fine = fine.to_dict() if fine else None
        split = [s.to_dict() for s in split] if split else None
        callback = callback.to_dict() if callback else None

        data = remove_none_and_empty_values(
            {
                'customer': customer,
                'billingType': billingType.value,
                'value': value,
                'dueDate': dueDate.strftime('%Y-%m-%d'),
                'description': description,
                'daysAfterDueDateToRegistrationCancellation': daysAfterDueDateToRegistrationCancellation,
                'externalReference': externalReference,
                'installmentCount': installmentCount,
                'totalValue': totalValue,
                'installmentValue': installmentValue,
                'discount': discount,
                'interest': interest,
                'fine': fine,
                'postalService': postalService,
                'split': split,
                'callback': callback
            }
        )

        response = self.asaas.post(f'{self.endpoint}', data)

        return self.response_data_to_payment(response.json())

    def list(
        self,
        customer: Optional[str] = None,
        customerGroupName: Optional[str] = None,
        billingType: Optional[payments.BillingType] = None,
        status: Optional[payments.Status] = None,
        subscription: Optional[str] = None,
        installment: Optional[str] = None,
        externalReference: Optional[str] = None,
        paymentDate: Optional[date] = None,
        invoiceStatus: Optional[str] = None,
        estimatedCreditDate: Optional[date] = None,
        pixQrCodeId: Optional[str] = None,
        antipated: Optional[bool] = None,
        dateCreatedGreaterThanOrEqual: Optional[date] = None,
        dateCreatedLessThanOrEqual: Optional[date] = None,
        paymentDateGreaterThanOrEqual: Optional[date] = None,
        paymentDateLessThanOrEqual: Optional[date] = None,
        estimatedCreditDateGreaterThanOrEqual: Optional[date] = None,
        estimatedCreditDateLessThanOrEqual: Optional[date] = None,
        dueDateGreaterThanOrEqual: Optional[date] = None,
        dueDateLessThanOrEqual: Optional[date] = None,
        user: Optional[str] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None
    ) -> List[payments.Payment]:
        """List payments"""

        params = remove_none_and_empty_values(
            {
                'customer': customer,
                'customerGroupName': customerGroupName,
                'billingType': billingType.value if billingType else None,
                'status': status.value if status else None,
                'subscription': subscription,
                'installment': installment,
                'externalReference': externalReference,
                'paymentDate': paymentDate,
                'invoiceStatus': invoiceStatus,
                'estimatedCreditDate': estimatedCreditDate,
                'pixQrCodeId': pixQrCodeId,
                'antipated': antipated,
                'dateCreatedGreaterThanOrEqual': dateCreatedGreaterThanOrEqual,
                'dateCreatedLessThanOrEqual': dateCreatedLessThanOrEqual,
                'paymentDateGreaterThanOrEqual': paymentDateGreaterThanOrEqual,
                'paymentDateLessThanOrEqual': paymentDateLessThanOrEqual,
                'estimatedCreditDateGreaterThanOrEqual': estimatedCreditDateGreaterThanOrEqual,
                'estimatedCreditDateLessThanOrEqual': estimatedCreditDateLessThanOrEqual,
                'dueDateGreaterThanOrEqual': dueDateGreaterThanOrEqual,
                'dueDateLessThanOrEqual': dueDateLessThanOrEqual,
                'user': user,
                'offset': offset,
                'limit': limit
            }
        )

        response = self.asaas.get(self.endpoint, params)

        return [self.response_data_to_payment(payment) for payment in response.json()['data']]

    def update(
        self,
        payment_id: str,
        value: Optional[float] = None,
        dueDate: Optional[date] = None,
        billingType: Optional[payments.BillingType] = None,
        description: Optional[str] = None,
        daysAfterDueDateToRegistrationCancellation: Optional[int] = None,
        externalReference: Optional[str] = None,
        installmentCount: Optional[int] = None,
        totalValue: Optional[float] = None,
        installmentValue: Optional[float] = None,
        discount: Optional[payments.Discount] = None,
        interest: Optional[payments.Interest] = None,
        fine: Optional[payments.Fine] = None,
        postalService: Optional[bool] = None,
        split: Optional[List[payments.Split]] = None,
        callback: Optional[payments.Callback] = None
    ) -> payments.Payment:

        discount = discount.to_dict() if discount else None
        interest = interest.to_dict() if interest else None
        fine = fine.to_dict() if fine else None
        split = [s.to_dict() for s in split] if split else None
        callback = callback.to_dict() if callback else None

        data = remove_none_and_empty_values(
            {
                'billingType': billingType.value,
                'value': value,
                'dueDate': dueDate.strftime('%Y-%m-%d') if dueDate else None,
                'description': description,
                'daysAfterDueDateToRegistrationCancellation': daysAfterDueDateToRegistrationCancellation,
                'externalReference': externalReference,
                'installmentCount': installmentCount,
                'totalValue': totalValue,
                'installmentValue': installmentValue,
                'discount': discount,
                'interest': interest,
                'fine': fine,
                'postalService': postalService,
                'split': split,
                'callback': callback
            }
        )

        response = self.asaas.put(
            f'{self.endpoint}/{payment_id}',
            data
        )

        return self.response_data_to_payment(response.json())

    def delete(
        self,
        payment_id: str
    ) -> None:
        """Delete a payment by ID"""

        self.asaas.delete(f'payments/{payment_id}')

    def restore(
        self,
        payment_id: str
    ) -> payments.Payment:
        """Restore a payment by ID"""

        response = self.asaas.post(f'{self.endpoint}/{payment_id}/restore')

        return self.response_data_to_payment(response.json())

    def retrieve_status(
        self,
        payment_id: str
    ) -> payments.Status:
        """Retrieve a payment status by ID"""

        response = self.asaas.get(f'{self.endpoint}/{payment_id}/status')

        return response.json()['status']

    def refund(
        self,
        payment_id: str,
        value: Optional[float] = None,
        description: Optional[str] = None
    ) -> payments.Payment:
        """payments.Refund a payment by ID"""

        data = remove_none_and_empty_values(
            {
                'value': value,
                'description': description
            }
        )

        response = self.asaas.post(
            f'{self.endpoint}/{payment_id}/refund', data)

        return self.response_data_to_payment(response.json())


class Subscriptions(ResponseDataToPayment):
    """Class to manage subscriptions in Asaas API"""

    def __init__(self, asaas: Asaas):
        self.asaas = asaas
        self.endpoint = 'subscriptions'

    def response_data_to_subscription(
        self,
        data: dict
    ):
        """Convert response data to Subscription object"""

        data['cicle'] = subscriptions.Cycle(
            **data['cicle']
        )

        data['status'] = subscriptions.Status(
            data['status']
        )

        data['discount'] = payments.Discount(
            **data['discount']
        ) if data.get('discount') else None

        data['interest'] = payments.Interest(
            **data['interest']
        ) if data.get('interest') else None

        data['fine'] = payments.Fine(
            **data['fine']) if data.get('fine') else None

        data['split'] = [
            payments.Split(**split) for split in data['split']
        ] if data.get('split') else None

        return subscriptions.Subscription(**data)

    def retrieve(
        self,
        subscription_id: str
    ) -> subscriptions.Subscription:
        """Retrieve a subscription by ID"""

        response = self.asaas.get(f'{self.endpoint}/{subscription_id}')

        return self.response_data_to_subscription(response.json())

    def create(
        self,
        customer: str,
        billingType: subscriptions.BillingType,
        value: float,
        nextDueDate: date,
        cycle: subscriptions.Cycle,
        discount: Optional[payments.Discount] = None,
        interest: Optional[payments.Interest] = None,
        fine: Optional[payments.Fine] = None,
        description: Optional[str] = None,
        endDate: Optional[date] = None,
        maxPayments: Optional[int] = None,
        externalReference: Optional[str] = None,
        split: Optional[List[payments.Split]] = None,
        callback: Optional[payments.Callback] = None
    ) -> subscriptions.Subscription:
        """Create a new subscription"""

        discount = discount.to_dict() if discount else None
        interest = interest.to_dict() if interest else None
        fine = fine.to_dict() if fine else None
        split = [s.to_dict() for s in split] if split else None
        callback = callback.to_dict() if callback else None

        data = remove_none_and_empty_values(
            {
                'customer': customer,
                'billingType': billingType.value,
                'value': value,
                'nextDueDate': nextDueDate.strftime('%Y-%m-%d'),
                'cycle': cycle,
                'discount': discount,
                'interest': interest,
                'fine': fine,
                'description': description,
                'endDate': endDate.strftime('%Y-%m-%d') if endDate else None,
                'maxPayments': maxPayments,
                'externalReference': externalReference,
                'split': split,
                'callback': callback
            }
        )

        response = self.asaas.post(f'{self.endpoint}', data)

        return self.response_data_to_subscription(response.json())

    def list(
        self,
        customer: Optional[str] = None,
        customerGroupName: Optional[str] = None,
        billingType: Optional[subscriptions.BillingType] = None,
        status: Optional[subscriptions.Status] = None,
        deletedOnly: Optional[bool] = None,
        includeDeleted: Optional[bool] = None,
        externalReference: Optional[str] = None,
        order: Optional[subscriptions.Order] = None,
        sort: Optional[subscriptions.Sort] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None
    ) -> List[subscriptions.Subscription]:
        """List subscriptions"""

        params = remove_none_and_empty_values(
            {
                'customer': customer,
                'customerGroupName': customerGroupName,
                'billingType': billingType.value if billingType else None,
                'status': status.value if status else None,
                'deletedOnly': deletedOnly,
                'includeDeleted': includeDeleted,
                'externalReference': externalReference,
                'order': order.value if order else None,
                'sort': sort.value if sort else None,
                'offset': offset,
                'limit': limit
            }
        )

        response = self.asaas.get(self.endpoint, params)

        return [self.response_data_to_subscription(subscription) for subscription in response.json()['data']]

    def update(
        self,
        subscription_id: str,
        billingType: Optional[subscriptions.BillingType] = None,
        value: Optional[float] = None,
        status: Optional[subscriptions.Status] = None,
        nextDueDate: Optional[date] = None,
        discount: Optional[payments.Discount] = None,
        interest: Optional[payments.Interest] = None,
        fine: Optional[payments.Fine] = None,
        cycle: Optional[subscriptions.Cycle] = None,
        description: Optional[str] = None,
        endDate: Optional[date] = None,
        updatePendingPayments: Optional[bool] = None,
        externalReference: Optional[str] = None,
        split: Optional[List[payments.Split]] = None,
        callback: Optional[payments.Callback] = None
    ) -> subscriptions.Subscription:
        """Update a subscription by ID"""

        discount = discount.to_dict() if discount else None
        interest = interest.to_dict() if interest else None
        fine = fine.to_dict() if fine else None
        split = [s.to_dict() for s in split] if split else None
        callback = callback.to_dict() if callback else None

        data = remove_none_and_empty_values(
            {
                'billingType': billingType.value if billingType else None,
                'value': value,
                'status': status.value if status else None,
                'nextDueDate': nextDueDate.strftime('%Y-%m-%d') if nextDueDate else None,
                'discount': discount,
                'interest': interest,
                'fine': fine,
                'cycle': cycle,
                'description': description,
                'endDate': endDate.strftime('%Y-%m-%d') if endDate else None,
                'updatePendingPayments': updatePendingPayments,
                'externalReference': externalReference,
                'split': split,
                'callback': callback
            }
        )

        response = self.asaas.put(
            f'{self.endpoint}/{subscription_id}',
            data
        )

        return self.response_data_to_subscription(response.json())

    def delete(
        self,
        subscription_id: str
    ) -> None:
        """Delete a subscription by ID"""

        self.asaas.delete(f'subscriptions/{subscription_id}')

    def list_payments(
        self,
        subscription_id: str,
        status: Optional[payments.Status] = None,
    ) -> List[payments.Payment]:
        """List payments of a subscription"""

        params = remove_none_and_empty_values(
            {
                'status': status.value if status else None,
            }
        )

        response = self.asaas.get(
            f'{self.endpoint}/{subscription_id}/payments', params)

        return self.response_data_to_payment(response.json()['data'])
