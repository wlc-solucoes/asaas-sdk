from asaas import (
    customer,
    payments,
    subscriptions,
    invoices
)
from asaas.objects import AsaasObject, AsaasList
from asaas.utils import remove_none_and_empty_values
from asaas.exceptions import raise_for_status, AsaasConnectionError

import requests

from typing import (
    Optional,
    List
)

from datetime import date


class Asaas:
    """SDK for Asaas API"""

    DEFAULT_USER_AGENT = 'asaas-sdk-wlc'

    def __init__(
        self,
        api_key: str,
        production: bool = False,
        user_agent: Optional[str] = None,
        timeout: Optional[float] = 30,
        session: Optional[requests.Session] = None
    ):
        self.base_url = 'https://api.asaas.com/v3' if production else 'https://api-sandbox.asaas.com/v3'
        # O User-Agent é obrigatório para contas raiz criadas a partir de 13/06/2024.
        self.headers = {
            'access_token': api_key,
            'User-Agent': user_agent or self.DEFAULT_USER_AGENT
        }
        self.timeout = timeout
        self.session = session or requests.Session()

        self.customers = Costumers(self)
        self.payments = Payments(self)
        self.subscriptions = Subscriptions(self)
        self.installments = Installments(self)
        self.invoices = Invoices(self)
        self.fiscal_info = FiscalInfo(self)
        self.webhooks = Webhooks(self)

    def request(
        self,
        method: str,
        endpoint: str,
        params: Optional[dict] = None,
        data: Optional[dict] = None,
        files: Optional[dict] = None
    ) -> requests.Response:
        """Make a request to Asaas API. GET never carries a body (Asaas answers 403)."""

        kwargs = {
            'headers': self.headers,
            'params': params,
            'timeout': self.timeout
        }
        if files is not None:
            kwargs['data'] = data
            kwargs['files'] = files
        elif data is not None:
            kwargs['json'] = data

        try:
            response = self.session.request(method, f'{self.base_url}/{endpoint}', **kwargs)
        except requests.RequestException as error:
            raise AsaasConnectionError(str(error)) from error

        raise_for_status(response)

        return response

    def get(
        self,
        endpoint: str,
        params: Optional[dict] = None
    ) -> requests.Response:
        """Make a GET request to Asaas API"""

        return self.request('GET', endpoint, params=params)

    def post(
        self,
        endpoint: str,
        data: Optional[dict] = None
    ) -> requests.Response:
        """Make a POST request to Asaas API"""

        return self.request('POST', endpoint, data=data if data is not None else {})

    def post_multipart(
        self,
        endpoint: str,
        data: dict,
        files: Optional[dict] = None
    ) -> requests.Response:
        """Make a multipart POST request to Asaas API (e.g. fiscal info with certificate)"""

        return self.request('POST', endpoint, data=data, files=files or {})

    def put(
        self,
        endpoint: str,
        data: dict
    ) -> requests.Response:
        """Make a PUT request to Asaas API"""

        return self.request('PUT', endpoint, data=data)

    def delete(
        self,
        endpoint: str
    ) -> requests.Response:
        """Make a DELETE request to Asaas API"""

        return self.request('DELETE', endpoint)


class Costumers:
    """Class to manage customers in Asaas API"""

    def __init__(self, asaas: Asaas):
        self.asaas = asaas
        self.endpoint = 'customers'
        
    
    def response_data_to_customer(
        self,
        data: dict
    ):
        return customer.Customer(**data)

    def retrieve(
        self,
        customer_id: str
    ) -> customer.Customer:
        """Retrieve a customer by ID"""

        response = self.asaas.get(f'{self.endpoint}/{customer_id}')

        return self.response_data_to_customer(response.json())

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

        return self.response_data_to_customer(response.json())

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

        return [self.response_data_to_customer(customer_dict) for customer_dict in response.json()['data']]

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

        return self.response_data_to_customer(response.json())

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

        return self.response_data_to_customer(response.json())


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
                'billingType': billingType,
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
                'billingType': billingType,
                'status': status,
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
                'billingType': billingType,
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


    def identification_field(
        self,
        payment_id: str
    ) -> AsaasObject:
        """Linha digitável do boleto: `identificationField`, `nossoNumero` e `barCode`.

        Não vem na criação da cobrança; consulte de novo após PAYMENT_UPDATED."""

        response = self.asaas.get(f'{self.endpoint}/{payment_id}/identificationField')

        return AsaasObject(response.json())

    def pix_qr_code(
        self,
        payment_id: str
    ) -> AsaasObject:
        """QR Code Pix da cobrança: `encodedImage` (base64), `payload` (copia e cola) e `expirationDate`"""

        response = self.asaas.get(f'{self.endpoint}/{payment_id}/pixQrCode')

        return AsaasObject(response.json())

    def receive_in_cash(
        self,
        payment_id: str,
        paymentDate: Optional[date] = None,
        value: Optional[float] = None,
        notifyCustomer: Optional[bool] = None
    ) -> payments.Payment:
        """Confirma o recebimento em dinheiro (fora do Asaas). Gera PAYMENT_RECEIVED."""

        data = remove_none_and_empty_values(
            {
                'paymentDate': paymentDate.strftime('%Y-%m-%d') if paymentDate else None,
                'value': value,
                'notifyCustomer': notifyCustomer
            }
        )

        response = self.asaas.post(f'{self.endpoint}/{payment_id}/receiveInCash', data)

        return self.response_data_to_payment(response.json())

    def undo_received_in_cash(
        self,
        payment_id: str
    ) -> payments.Payment:
        """Desfaz a confirmação de recebimento em dinheiro. Gera PAYMENT_RECEIVED_IN_CASH_UNDONE."""

        response = self.asaas.post(f'{self.endpoint}/{payment_id}/undoReceivedInCash')

        return self.response_data_to_payment(response.json())

    def list_page(
        self,
        **filters
    ) -> AsaasList:
        """Lista cobranças devolvendo a página (`has_more`, `total_count`) como dicionários"""

        response = self.asaas.get(self.endpoint, remove_none_and_empty_values(filters))

        return AsaasList(response.json())


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

        data['discount'] = payments.Discount(
            **data['discount']
        ) if data.get('discount') else None

        data['interest'] = payments.Interest(
            **data['interest']
        ) if data.get('interest') else None

        data['fine'] = payments.Fine(
            **data['fine']
        ) if data.get('fine') else None

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
                'billingType': billingType,
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
                'billingType': billingType,
                'status': status,
                'deletedOnly': deletedOnly,
                'includeDeleted': includeDeleted,
                'externalReference': externalReference,
                'order': order,
                'sort': sort,
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
                'billingType': billingType,
                'value': value,
                'status': status,
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
                'status': status,
            }
        )

        response = self.asaas.get(
            f'{self.endpoint}/{subscription_id}/payments', params)

        return [self.response_data_to_payment(payment) for payment in response.json()['data']]


class Installments(ResponseDataToPayment):
    """Parcelamentos (carnê). Todas as parcelas têm o mesmo valor e vencem no mesmo dia do mês."""

    def __init__(self, asaas: Asaas):
        self.asaas = asaas
        self.endpoint = 'installments'

    def create(
        self,
        customer: str,
        installmentCount: int,
        dueDate: date,
        billingType: str = payments.BillingType.BOLETO,
        value: Optional[float] = None,
        totalValue: Optional[float] = None,
        description: Optional[str] = None,
        paymentExternalReference: Optional[str] = None,
        daysAfterDueDateToRegistrationCancellation: Optional[int] = None,
        postalService: Optional[bool] = None,
        discount: Optional[payments.Discount] = None,
        interest: Optional[payments.Interest] = None,
        fine: Optional[payments.Fine] = None
    ) -> AsaasObject:
        """Cria um parcelamento. `value` é o valor de CADA parcela; `totalValue` divide o total
        (a diferença de arredondamento fica na última). `dueDate` é o vencimento da primeira."""

        if installmentCount < 2:
            raise ValueError('Parcelamento precisa de ao menos 2 parcelas; use payments.create.')
        if (value is None) == (totalValue is None):
            raise ValueError('Informe value (por parcela) ou totalValue, não os dois.')

        data = remove_none_and_empty_values(
            {
                'customer': customer,
                'billingType': billingType,
                'installmentCount': installmentCount,
                'value': value,
                'totalValue': totalValue,
                'dueDate': dueDate.strftime('%Y-%m-%d'),
                'description': description,
                'paymentExternalReference': paymentExternalReference,
                'daysAfterDueDateToRegistrationCancellation': daysAfterDueDateToRegistrationCancellation,
                'postalService': postalService,
                'discount': discount.to_dict() if discount else None,
                'interest': interest.to_dict() if interest else None,
                'fine': fine.to_dict() if fine else None
            }
        )

        response = self.asaas.post(self.endpoint, data)

        return AsaasObject(response.json())

    def retrieve(
        self,
        installment_id: str
    ) -> AsaasObject:
        """Recupera um parcelamento"""

        response = self.asaas.get(f'{self.endpoint}/{installment_id}')

        return AsaasObject(response.json())

    def list_payments(
        self,
        installment_id: str,
        status: Optional[str] = None
    ) -> List[payments.Payment]:
        """Cobranças do parcelamento, na ordem das parcelas"""

        response = self.asaas.get(
            f'{self.endpoint}/{installment_id}/payments',
            remove_none_and_empty_values({'status': status})
        )
        items = [self.response_data_to_payment(payment) for payment in response.json()['data']]

        return sorted(items, key=lambda payment: (payment.installmentNumber or 0, payment.dueDate))

    def payment_book(
        self,
        installment_id: str,
        sort: Optional[str] = None,
        order: Optional[str] = None
    ) -> bytes:
        """PDF do carnê (application/pdf)"""

        response = self.asaas.get(
            f'{self.endpoint}/{installment_id}/paymentBook',
            remove_none_and_empty_values({'sort': sort, 'order': order})
        )

        return response.content

    def delete(
        self,
        installment_id: str
    ) -> None:
        """Remove o parcelamento e suas cobranças pendentes"""

        self.asaas.delete(f'{self.endpoint}/{installment_id}')


class Invoices:
    """Notas fiscais de serviço (NFS-e) emitidas pelo Asaas"""

    def __init__(self, asaas: Asaas):
        self.asaas = asaas
        self.endpoint = 'invoices'

    def schedule(
        self,
        serviceDescription: str,
        value: float,
        effectiveDate: date,
        taxes: invoices.Taxes,
        payment: Optional[str] = None,
        installment: Optional[str] = None,
        customer: Optional[str] = None,
        observations: str = '',
        deductions: float = 0,
        municipalServiceId: Optional[str] = None,
        municipalServiceCode: Optional[str] = None,
        municipalServiceName: Optional[str] = None,
        externalReference: Optional[str] = None,
        updatePayment: Optional[bool] = None
    ) -> AsaasObject:
        """Agenda uma nota (status SCHEDULED). Informe payment, installment ou customer, e
        municipalServiceId ou municipalServiceCode. Para emitir na hora, chame `authorize`."""

        if not (payment or installment or customer):
            raise ValueError('Informe payment, installment ou customer.')
        if not (municipalServiceId or municipalServiceCode):
            raise ValueError('Informe municipalServiceId ou municipalServiceCode.')

        data = {
            'serviceDescription': serviceDescription,
            'observations': observations or '',
            'value': value,
            'deductions': deductions or 0,
            'effectiveDate': effectiveDate.strftime('%Y-%m-%d'),
            'municipalServiceName': municipalServiceName or municipalServiceCode or '',
            'taxes': taxes.to_dict(),
            **remove_none_and_empty_values(
                {
                    'payment': payment,
                    'installment': installment,
                    'customer': customer,
                    'municipalServiceId': municipalServiceId,
                    'municipalServiceCode': municipalServiceCode,
                    'externalReference': externalReference,
                    'updatePayment': updatePayment
                }
            )
        }

        response = self.asaas.post(self.endpoint, data)

        return AsaasObject(response.json())

    def create(self, data: dict) -> AsaasObject:
        """Agenda uma nota com o corpo pronto (montado pelo consumidor)"""

        response = self.asaas.post(self.endpoint, data)

        return AsaasObject(response.json())

    def retrieve(
        self,
        invoice_id: str
    ) -> AsaasObject:
        """Recupera uma nota"""

        response = self.asaas.get(f'{self.endpoint}/{invoice_id}')

        return AsaasObject(response.json())

    def list(
        self,
        **filters
    ) -> AsaasList:
        """Lista notas (filtros: payment, installment, customer, externalReference, status,
        effectiveDate[ge]/[le], offset, limit)"""

        response = self.asaas.get(self.endpoint, remove_none_and_empty_values(filters))

        return AsaasList(response.json())

    def update(
        self,
        invoice_id: str,
        data: dict
    ) -> AsaasObject:
        """Atualiza uma nota agendada"""

        response = self.asaas.put(f'{self.endpoint}/{invoice_id}', data)

        return AsaasObject(response.json())

    def authorize(
        self,
        invoice_id: str
    ) -> AsaasObject:
        """Antecipa a emissão de uma nota agendada. A autorização chega por INVOICE_AUTHORIZED."""

        response = self.asaas.post(f'{self.endpoint}/{invoice_id}/authorize')

        return AsaasObject(response.json())

    def cancel(
        self,
        invoice_id: str,
        cancelOnlyOnAsaas: Optional[bool] = None
    ) -> AsaasObject:
        """Cancela uma nota. O resultado chega por INVOICE_CANCELED/INVOICE_CANCELLATION_DENIED."""

        response = self.asaas.post(
            f'{self.endpoint}/{invoice_id}/cancel',
            remove_none_and_empty_values({'cancelOnlyOnAsaas': cancelOnlyOnAsaas})
        )

        return AsaasObject(response.json())


class FiscalInfo:
    """Dados fiscais da conta para emissão de NFS-e"""

    def __init__(self, asaas: Asaas):
        self.asaas = asaas
        self.endpoint = 'fiscalInfo'

    def retrieve(self) -> AsaasObject:
        """Dados fiscais salvos (segredos voltam só como `*Sent`)"""

        response = self.asaas.get(f'{self.endpoint}/')

        return AsaasObject(response.json())

    def save(
        self,
        email: str,
        simplesNacional: bool,
        municipalInscription: Optional[str] = None,
        culturalProjectsPromoter: Optional[bool] = None,
        cnae: Optional[str] = None,
        specialTaxRegime: Optional[str] = None,
        serviceListItem: Optional[str] = None,
        nbsCode: Optional[str] = None,
        rpsSerie: Optional[str] = None,
        rpsNumber: Optional[int] = None,
        loteNumber: Optional[int] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        accessToken: Optional[str] = None,
        certificateFile: Optional[bytes] = None,
        certificatePassword: Optional[str] = None,
        nationalPortalTaxCalculationRegime: Optional[str] = None,
        serviceProvisionCityDefaultType: Optional[str] = None
    ) -> AsaasObject:
        """Cria/atualiza os dados fiscais (multipart). Envie só a credencial que
        `municipal_options().authenticationType` pede."""

        data = remove_none_and_empty_values(
            {
                'email': email,
                'simplesNacional': str(bool(simplesNacional)).lower(),
                'municipalInscription': municipalInscription,
                'culturalProjectsPromoter': (
                    str(bool(culturalProjectsPromoter)).lower() if culturalProjectsPromoter is not None else None
                ),
                'cnae': cnae,
                'specialTaxRegime': specialTaxRegime,
                'serviceListItem': serviceListItem,
                'nbsCode': nbsCode,
                'rpsSerie': rpsSerie,
                'rpsNumber': rpsNumber,
                'loteNumber': loteNumber,
                'username': username,
                'password': password,
                'accessToken': accessToken,
                'certificatePassword': certificatePassword,
                'nationalPortalTaxCalculationRegime': nationalPortalTaxCalculationRegime,
                'serviceProvisionCityDefaultType': serviceProvisionCityDefaultType
            }
        )
        files = {'certificateFile': ('certificado.pfx', certificateFile)} if certificateFile else None

        response = self.asaas.post_multipart(f'{self.endpoint}/', data, files)

        return AsaasObject(response.json())

    def municipal_options(self) -> AsaasObject:
        """O que o município da conta exige (authenticationType, supportsCancellation, regimes...)"""

        response = self.asaas.get(f'{self.endpoint}/municipalOptions')

        return AsaasObject(response.json())

    def services(
        self,
        description: Optional[str] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None
    ) -> AsaasList:
        """Serviços municipais (`id`, `description`, `issTax`); o `id` vai em municipalServiceId"""

        response = self.asaas.get(
            f'{self.endpoint}/services',
            remove_none_and_empty_values({'description': description, 'offset': offset, 'limit': limit})
        )

        return AsaasList(response.json())


class Webhooks:
    """Configuração de webhooks da conta (até 10 por conta)"""

    def __init__(self, asaas: Asaas):
        self.asaas = asaas
        self.endpoint = 'webhooks'

    def create(
        self,
        name: str,
        url: str,
        email: str,
        events: List[str],
        authToken: Optional[str] = None,
        enabled: bool = True,
        interrupted: bool = False,
        sendType: str = 'SEQUENTIALLY',
        apiVersion: int = 3
    ) -> AsaasObject:
        """Cria um webhook. Sem `authToken`, o Asaas gera um e devolve UMA vez na resposta."""

        data = remove_none_and_empty_values(
            {
                'name': name,
                'url': url,
                'email': email,
                'events': events,
                'authToken': authToken,
                'enabled': enabled,
                'interrupted': interrupted,
                'sendType': sendType,
                'apiVersion': apiVersion
            }
        )

        response = self.asaas.post(self.endpoint, data)

        return AsaasObject(response.json())

    def list(self) -> AsaasList:
        """Webhooks da conta"""

        response = self.asaas.get(self.endpoint)

        return AsaasList(response.json())

    def retrieve(self, webhook_id: str) -> AsaasObject:
        response = self.asaas.get(f'{self.endpoint}/{webhook_id}')

        return AsaasObject(response.json())

    def update(self, webhook_id: str, data: dict) -> AsaasObject:
        response = self.asaas.put(f'{self.endpoint}/{webhook_id}', data)

        return AsaasObject(response.json())

    def delete(self, webhook_id: str) -> None:
        self.asaas.delete(f'{self.endpoint}/{webhook_id}')
