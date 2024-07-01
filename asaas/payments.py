from typing import Optional
from datetime import date
from enum import Enum


class Status(Enum):
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


class BillingType(Enum):
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
        type: Type,
        **kwargs
    ) -> None:
        self.value = value
        self.dueDateLimitDays = dueDateLimitDays
        self.type = type

    def to_dict(self) -> dict:
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
        **kwargs
    ) -> None:
        self.value = value

    def to_dict(self) -> dict:
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
        type: Type,
        **kwargs
    ) -> None:

        self.value = value
        self.type = type

    def to_dict(self) -> dict:
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
        transactionReceiptUrl: str,
        **kwargs
    ) -> None:
        self.dateCreated = dateCreated
        self.status = status
        self.value = value
        self.description = description
        self.transactionReceiptUrl = transactionReceiptUrl

    def to_dict(self) -> dict:
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
        totalFixedValue: Optional[float] = None,
        **kwargs
    ) -> None:
        self.walletId = walletId
        self.fixedValue = fixedValue
        self.percentageValue = percentageValue
        self.totalFixedValue = totalFixedValue

    def to_dict(self) -> dict:
        return {
            'walletId': self.walletId,
            'fixedValue': self.fixedValue,
            'percentageValue': self.percentageValue,
            'totalFixedValue': self.totalFixedValue
        }


class Chargeback:
    """Chargeback object for payment"""

    class Status(Enum):
        """Status for chargeback"""
        REQUESTED = 'REQUESTED'
        IN_DISPUTE = 'IN_DISPUTE'
        DISPUTE_LOST = 'DISPUTE_LOST'
        REVERSED = 'REVERSED'
        DONE = 'DONE'

    class Reason(Enum):
        """Reason for chargeback"""
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

    def to_dict(self) -> dict:
        return {
            'sucessUrl': self.sucessUrl,
            'autoRedirect': self.autoRedirect
        }


class Payment:
    """ Payment object for Asaas API """

    def __init__(
        self,
        id: str,
        customer: str,
        dateCreated: date,
        dueDate: date,
        value: float,
        installment: Optional[str] = None,
        subscription: Optional[str] = None,
        paymentLink: Optional[str] = None,
        netValue: Optional[float] = None,
        billingType: Optional[BillingType] = None,
        status: Optional[Status] = None,
        description: Optional[str] = None,
        externalReference: Optional[str] = None,
        canBePaidAfterDueDate: Optional[bool] = None,
        pixTransaction: Optional[str] = None,
        pixQrCodeId: Optional[str] = None,
        originalValue: Optional[float] = None,
        interestValue: Optional[float] = None,
        originalDueDate: Optional[date] = None,
        paymentDate: Optional[date] = None,
        clientPaymentDate: Optional[date] = None,
        installmentNumber: Optional[int] = None,
        transactionReceiptUrl: Optional[str] = None,
        duplicatedPayment: Optional[str] = None,
        nossoNumero: Optional[str] = None,
        invoiceUrl: Optional[str] = None,
        bankSlipUrl: Optional[str] = None,
        invoiceNumber: Optional[str] = None,
        discount: Optional[Discount] = None,
        fine: Optional[Fine] = None,
        interest: Optional[Interest] = None,
        deleted: Optional[bool] = None,
        postalService: Optional[bool] = None,
        anticipated: Optional[bool] = None,
        anticipable: Optional[bool] = None,
        refunds: Optional[list[Refund]] = [],
        split: Optional[list[Split]] = [],
        **kwargs
    ):
        self.id = id
        self.customer = customer
        self.dateCreated = dateCreated if type(
            dateCreated) == date else date.fromisoformat(dateCreated)
        self.dueDate = dueDate if type(
            dueDate) == date else date.fromisoformat(dueDate)
        self.value = value
        self.installment = installment
        self.subscription = subscription
        self.paymentLink = paymentLink
        self.netValue = netValue
        self.billingType = billingType
        self.status = status
        self.description = description
        self.externalReference = externalReference
        self.canBePaidAfterDueDate = canBePaidAfterDueDate
        self.pixTransaction = pixTransaction
        self.pixQrCodeId = pixQrCodeId
        self.originalValue = originalValue
        self.interestValue = interestValue

        self.originalDueDate = originalDueDate if type(
            originalDueDate) == date else date.fromisoformat(originalDueDate) if originalDueDate else None

        self.paymentDate = paymentDate if type(
            paymentDate) == date else date.fromisoformat(paymentDate) if paymentDate else None

        self.clientPaymentDate = clientPaymentDate if type(
            clientPaymentDate) == date else date.fromisoformat(clientPaymentDate) if clientPaymentDate else None

        self.installmentNumber = installmentNumber
        self.transactionReceiptUrl = transactionReceiptUrl
        self.duplicatedPayment = duplicatedPayment
        self.nossoNumero = nossoNumero
        self.invoiceUrl = invoiceUrl
        self.bankSlipUrl = bankSlipUrl
        self.invoiceNumber = invoiceNumber
        self.discount = discount
        self.fine = fine
        self.interest = interest
        self.deleted = deleted
        self.postalService = postalService
        self.anticipated = anticipated
        self.anticipable = anticipable
        self.refunds = refunds
        self.split = split

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'customer': self.customer,
            'dateCreated': self.dateCreated.strftime('%Y-%m-%d'),
            'dueDate': self.dueDate.strftime('%Y-%m-%d'),
            'value': self.value,
            'installment': self.installment,
            'subscription': self.subscription,
            'paymentLink': self.paymentLink,
            'netValue': self.netValue,
            'billingType': self.billingType,
            'status': self.status,
            'description': self.description,
            'externalReference': self.externalReference,
            'canBePaidAfterDueDate': self.canBePaidAfterDueDate,
            'pixTransaction': self.pixTransaction,
            'pixQrCodeId': self.pixQrCodeId,
            'originalValue': self.originalValue,
            'interestValue': self.interestValue,
            'originalDueDate': self.originalDueDate.strftime('%Y-%m-%d') if self.originalDueDate else None,
            'paymentDate': self.paymentDate.strftime('%Y-%m-%d') if self.paymentDate else None,
            'clientPaymentDate': self.clientPaymentDate.strftime('%Y-%m-%d') if self.clientPaymentDate else None,
            'installmentNumber': self.installmentNumber,
            'transactionReceiptUrl': self.transactionReceiptUrl,
            'duplicatedPayment': self.duplicatedPayment,
            'nossoNumero': self.nossoNumero,
            'invoiceUrl': self.invoiceUrl,
            'bankSlipUrl': self.bankSlipUrl,
            'invoiceNumber': self.invoiceNumber,
            'discount': self.discount.to_dict() if self.discount else None,
            'fine': self.fine.to_dict() if self.fine else None,
            'interest': self.interest.to_dict() if self.interest else None,
            'deleted': self.deleted,
            'postalService': self.postalService,
            'anticipated': self.anticipated,
            'anticipable': self.anticipable,
            'refunds': [refund.to_dict() for refund in self.refunds] if self.refunds else None,
            'split': [split.to_dict() for split in self.split] if self.split else None
        }
