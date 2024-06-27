from typing import Optional


class BillingType:
    """Billing type for payment"""

    UNDEFINED = 'UNDEFINED'
    BOLETO = 'BOLETO'
    CREDIT_CARD = 'CREDIT_CARD'
    PIX = 'PIX'


class Discount:
    """Discount object for payment"""

    class Type:
        """Type of discount"""

        FIXED = 'FIXED'
        PERCENTAGE = 'PERCENTAGE'

    def __init__(
        self,
        value: int,
        dueDateLimitDays: int,
        type: Type
    ) -> None:
        self.value = value
        self.dueDateLimitDays = dueDateLimitDays
        self.type = type

    def to_json(self) -> dict:
        return {
            'value': self.value,
            'dueDateLimitDays': self.dueDateLimitDays,
            'type': self.type
        }


class Interest:
    """Interest object for payment"""

    def __init__(
        self,
        value: float,
    ) -> None:
        self.value = value

    def to_json(self) -> dict:
        return {
            'value': self.value,
        }


class Fine:
    """Fine object for payment"""

    class Type:
        FIXED = 'FIXED'
        PERCENTAGE = 'PERCENTAGE'

    def __init__(
        self,
        value: float,
        type: Type
    ) -> None:

        self.value = value
        self.type = type

    def to_json(self) -> dict:
        return {
            'value': self.value,
            'type': self.type
        }


class Split:
    """Split object for payment"""

    def __init__(
        self,
        walletId: str,
        fixedValue: Optional[float] = None,
        percentageValue: Optional[float] = None,
        totalFixedValue: Optional[float] = None
    ) -> None:
        self.walletId = walletId
        self.fixedValue = fixedValue
        self.percentageValue = percentageValue
        self.totalFixedValue = totalFixedValue

    def to_json(self) -> dict:
        return {
            'walletId': self.walletId,
            'fixedValue': self.fixedValue,
            'percentageValue': self.percentageValue,
            'totalFixedValue': self.totalFixedValue
        }


class Callback:
    """Callback object for payment"""

    def __init__(
        self,
        sucessUrl: str,
        autoRedirect: Optional[bool] = True
    ) -> None:
        self.sucessUrl = sucessUrl
        self.autoRedirect = autoRedirect

    def to_json(self) -> dict:
        return {
            'sucessUrl': self.sucessUrl,
            'autoRedirect': self.autoRedirect
        }
