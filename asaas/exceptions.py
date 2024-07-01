from asaas import status

from requests import Response
from requests.exceptions import HTTPError


def raise_for_status(response: Response):

    if response.status_code == status.HTTP_400_BAD_REQUEST:
        error = response.json().get('errors')[0]

        code = error.get('code')
        description = error.get('description')

        error_match = {
            'invalid_action': InvalidActionAsaas,
            'invalid_creditCard': InvalidCreditCardAsaas,
            'invalid_value': InvalidValueAsaas,
            'invalid_billingType': InvalidBillingTypeAsaas,
            'invalid_customer': InvalidCustomerAsaas,
            'invalid_dueDate': InvalidDueDateAsaas,
            'invalid_name': InvalidNameAsaas
        }

        raise error_match.get(code, AsaasError)(description)

    elif response.status_code == status.HTTP_404_NOT_FOUND:
        raise NotFoundAsaas(response.url)

    try:
        response.raise_for_status()

    except HTTPError as error:
        raise AsaasError(error)


class AsaasError(Exception):
    pass


class InvalidActionAsaas(AsaasError):
    pass


class InvalidCreditCardAsaas(AsaasError):
    pass


class InvalidValueAsaas(AsaasError):
    pass


class InvalidBillingTypeAsaas(AsaasError):
    pass


class InvalidCustomerAsaas(AsaasError):
    pass


class InvalidDueDateAsaas(AsaasError):
    pass


class InvalidNameAsaas(AsaasError):
    pass


class NotFoundAsaas(AsaasError):
    pass
