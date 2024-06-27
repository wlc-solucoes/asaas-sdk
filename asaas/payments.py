from typing import Optional


class Status:
    """Status for payment"""

    PENDING = 'PENDING'
    RECEIVED = 'RECEIVED'
    CONFIRMED = 'CONFIRMED'
    OVERDUE = 'OVERDUE'
    REFUNDED = 'REFUNDED'
    RECEIVED_IN_CASH = 'RECEIVED_IN_CASH'
    REFUND_REQUESTED = 'REFUND_REQUESTED'
    REFUND_IN_PROGRESS = 'REFUND_IN_PROGRESS'
    CHARGEBACK_REQUESTED = 'CHARGEBACK_REQUESTED'
    CHARGEBACK_DISPUTE = 'CHARGEBACK_DISPUTE'
    AWAITING_CHARGEBACK_REVERSAL = 'AWAITING_CHARGEBACK_REVERSAL'
    DUNNING_REQUESTED = 'DUNNING_REQUESTED'
    DUNNING_RECEIVED = 'DUNNING_RECEIVED'
    AWAITING_RISK_ANALYSIS = 'AWAITING_RISK_ANALYSIS'


class BillingType:
    """Billing type for payment"""

    BOLETO = 'BOLETO'
    CREDIT_CARD = 'CREDIT_CARD'
    UNDEFINED = 'UNDEFINED'
    DEBIT_CARD = 'DEBIT_CARD'
    TRANSFER = 'TRANSFER'
    DEPOSIT = 'DEPOSIT'
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


class Refund:
    class Status:
        PENDING = 'PENDING'
        CANCELLED = 'CANCELLED'
        DONE = 'DONE'

    def __init__(
        self,
        dateCreated: str,
        status: Status,
        value: float,
        description: str,
        transactionReceiptUrl: str
    ) -> None:
        self.dateCreated = dateCreated
        self.status = status
        self.value = value
        self.description = description
        self.transactionReceiptUrl = transactionReceiptUrl

    def to_json(self) -> dict:
        return {
            'dateCreated': self.dateCreated,
            'status': self.status,
            'value': self.value,
            'description': self.description,
            'transactionReceiptUrl': self.transactionReceiptUrl
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


class Chargeback:
    class Status:
        REQUESTED = 'REQUESTED'
        IN_DISPUTE = 'IN_DISPUTE'
        DISPUTE_LOST = 'DISPUTE_LOST'
        REVERSED = 'REVERSED'
        DONE = 'DONE'

    class Reason:
        ABSENCE_OF_PRINT = 'ABSENCE_OF_PRINT'
        ABSENT_CARD_FRAUD = 'ABSENT_CARD_FRAUD'
        CARD_ACTIVATED_PHONE_TRANSACTION = 'CARD_ACTIVATED_PHONE_TRANSACTION'
        CARD_FRAUD = 'CARD_FRAUD'
        CARD_RECOVERY_BULLETIN = 'CARD_RECOVERY_BULLETIN'
        COMMERCIAL_DISAGREEMENT = 'COMMERCIAL_DISAGREEMENT'
        COPY_NOT_RECEIVED = 'COPY_NOT_RECEIVED'
        CREDIT_OR_DEBIT_PRESENTATION_ERROR = 'CREDIT_OR_DEBIT_PRESENTATION_ERROR'
        DIFFERENT_PAY_METHOD = 'DIFFERENT_PAY_METHOD'
        FRAUD = 'FRAUD'
        INCORRECT_TRANSACTION_VALUE = 'INCORRECT_TRANSACTION_VALUE'
        INVALID_CURRENCY = 'INVALID_CURRENCY'
        INVALID_DATA = 'INVALID_DATA'
        LATE_PRESENTATION = 'LATE_PRESENTATION'
        LOCAL_REGULATORY_OR_LEGAL_DISPUTE = 'LOCAL_REGULATORY_OR_LEGAL_DISPUTE'
        MULTIPLE_ROCS = 'MULTIPLE_ROCS'
        ORIGINAL_CREDIT_TRANSACTION_NOT_ACCEPTED = 'ORIGINAL_CREDIT_TRANSACTION_NOT_ACCEPTED'
        OTHER_ABSENT_CARD_FRAUD = 'OTHER_ABSENT_CARD_FRAUD'
        PROCESS_ERROR = 'PROCESS_ERROR'
        RECEIVED_COPY_ILLEGIBLE_OR_INCOMPLETE = 'RECEIVED_COPY_ILLEGIBLE_OR_INCOMPLETE'
        RECURRENCE_CANCELED = 'RECURRENCE_CANCELED'
        REQUIRED_AUTHORIZATION_NOT_GRANTED = 'REQUIRED_AUTHORIZATION_NOT_GRANTED'
        RIGHT_OF_FULL_RECOURSE_FOR_FRAUD = 'RIGHT_OF_FULL_RECOURSE_FOR_FRAUD'
        SALE_CANCELED = 'SALE_CANCELED'
        SERVICE_DISAGREEMENT_OR_DEFECTIVE_PRODUCT = 'SERVICE_DISAGREEMENT_OR_DEFECTIVE_PRODUCT'
        SERVICE_NOT_RECEIVED = 'SERVICE_NOT_RECEIVED'
        SPLIT_SALE = 'SPLIT_SALE'
        TRANSFERS_OF_DIVERSE_RESPONSIBILITIES = 'TRANSFERS_OF_DIVERSE_RESPONSIBILITIES'
        UNQUALIFIED_CAR_RENTAL_DEBIT = 'UNQUALIFIED_CAR_RENTAL_DEBIT'
        USA_CARDHOLDER_DISPUTE = 'USA_CARDHOLDER_DISPUTE'
        VISA_FRAUD_MONITORING_PROGRAM = 'VISA_FRAUD_MONITORING_PROGRAM'
        WARNING_BULLETIN_FILE = 'WARNING_BULLETIN_FILE'


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
