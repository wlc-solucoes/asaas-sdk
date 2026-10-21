from asaas import status

from requests import Response
from requests.exceptions import HTTPError


def _errors_from(response: Response) -> list:
    try:
        return (response.json() or {}).get('errors') or []
    except ValueError:
        return []


def raise_for_status(response: Response):

    if response.status_code == status.HTTP_400_BAD_REQUEST:
        errors = _errors_from(response)
        error = errors[0] if errors else {}

        code = error.get('code')
        description = '; '.join(
            item.get('description') for item in errors if item.get('description')
        ) or 'Requisição inválida para o Asaas.'

        error_match = {
            'invalid_action': InvalidActionAsaas,
            'invalid_creditCard': InvalidCreditCardAsaas,
            'invalid_value': InvalidValueAsaas,
            'invalid_billingType': InvalidBillingTypeAsaas,
            'invalid_customer': InvalidCustomerAsaas,
            'invalid_dueDate': InvalidDueDateAsaas,
            'invalid_name': InvalidNameAsaas
        }

        raise error_match.get(code, AsaasError)(
            description, code=code, status_code=response.status_code, errors=errors
        )

    elif response.status_code == status.HTTP_401_UNAUTHORIZED:
        errors = _errors_from(response)
        code = errors[0].get('code') if errors else None
        raise AuthenticationAsaas(
            'Chave de API do Asaas inválida ou de outro ambiente.',
            code=code, status_code=response.status_code, errors=errors
        )

    elif response.status_code == status.HTTP_404_NOT_FOUND:
        raise NotFoundAsaas(response.url, status_code=response.status_code)

    elif response.status_code == status.HTTP_429_TOO_MANY_REQUESTS:
        raise RateLimitAsaas(
            'Limite de requisições do Asaas atingido.',
            status_code=response.status_code,
            errors=_errors_from(response)
        )

    try:
        response.raise_for_status()

    except HTTPError as error:
        raise AsaasError(error, status_code=response.status_code, errors=_errors_from(response))


class AsaasError(Exception):

    def __init__(self, message='', code=None, status_code=None, errors=None):
        super().__init__(message)
        self.message = str(message)
        self.code = code
        self.status_code = status_code
        self.errors = errors or []


class AsaasConnectionError(AsaasError):
    """Falha de rede/timeout: a requisição pode ou não ter chegado ao Asaas."""
    pass


class AuthenticationAsaas(AsaasError):
    pass


class RateLimitAsaas(AsaasError):
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
