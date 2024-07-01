from enum import Enum
from typing import Optional
from asaas import payments

from datetime import date


class Cycle:
    """Cycle for payment of subscription"""

    WEEKLY = 'WEEKLY'
    BIWEEKLY = 'BIWEEKLY'
    MONTHLY = 'MONTHLY'
    BIMONTHLY = 'BIMONTHLY'
    QUARTERLY = 'QUARTERLY'
    SEMIANNUALLY = 'SEMIANNUALLY'
    ANNUALLY = 'ANNUALLY'


class BillingType(Enum):
    """Billing type for payment of subscription"""

    BOLETO = 'BOLETO'
    CREDIT_CARD = 'CREDIT_CARD'
    UNDEFINED = 'UNDEFINED'
    PIX = 'PIX'


class Status(Enum):
    """Status of subscription"""

    ACTIVE = 'ACTIVE'
    INACTIVE = 'INACTIVE'
    EXPIRED = 'EXPIRED'


class Order(Enum):
    """Order for subscription"""

    ASC = 'asc'
    DESC = 'desc'


class Sort(Enum):
    """Sort for subscription"""

    ID = 'id'
    DATE_CREATED = 'dateCreated'
    CUSTOMER = 'customer'
    PAYMENT_LINK = 'paymentLink'
    VALUE = 'value'
    NEXT_DUE_DATE = 'nextDueDate'
    CYCLE = 'cycle'
    DESCRIPTION = 'description'
    BILLING_TYPE = 'billingType'
    DELETED = 'deleted'
    STATUS = 'status'
    EXTERNAL_REFERENCE = 'externalReference'
    SEND_PAYMENT_BY_POSTAL_SERVICE = 'sendPaymentByPostalService'
    FINE = 'fine'
    INTEREST = 'interest'
    SPLIT = 'split'


class Subscription:

    def __init__(
        self,
        id: str,
        dateCreated: date,
        customer: str,
        billingType: BillingType,
        cycle: Cycle,
        value: float,
        nextDueDate: date,
        status: Status,
        endDate: Optional[date] = None,
        paymentLink: Optional[str] = None,
        description: Optional[str] = None,
        discount: Optional[payments.Discount] = None,
        fine: Optional[payments.Fine] = None,
        interest: Optional[payments.Interest] = None,
        deleted: Optional[bool] = None,
        maxPayments: Optional[int] = None,
        externalReference: Optional[str] = None,
        split: Optional[list[payments.Split]] = None
    ):
        self.id = id

        self.dateCreated = dateCreated if type(
            dateCreated) == date else date.fromisoformat(dateCreated)

        self.customer = customer
        self.billingType = billingType
        self.cycle = cycle
        self.value = value

        self.nextDueDate = nextDueDate if type(
            nextDueDate) == date else date.fromisoformat(nextDueDate)

        self.status = status

        self.endDate = endDate if type(endDate) == date else date.fromisoformat(
            endDate) if endDate else None

        self.paymentLink = paymentLink
        self.description = description
        self.discount = discount
        self.fine = fine
        self.interest = interest
        self.deleted = deleted
        self.maxPayments = maxPayments
        self.externalReference = externalReference
        self.split = split

    def to_dict(self):
        return {
            'id': self.id,
            'dateCreated': self.dateCreated.isoformat(),
            'customer': self.customer,
            'billingType': self.billingType.value,
            'cycle': self.cycle,
            'value': self.value,
            'nextDueDate': self.nextDueDate.isoformat(),
            'status': self.status.value,
            'endDate': self.endDate.isoformat() if self.endDate else None,
            'paymentLink': self.paymentLink,
            'description': self.description,
            'discount': self.discount.to_dict() if self.discount else None,
            'fine': self.fine.to_dict() if self.fine else None,
            'interest': self.interest.to_dict() if self.interest else None,
            'deleted': self.deleted,
            'maxPayments': self.maxPayments,
            'externalReference': self.externalReference,
            'split': [s.to_dict() for s in self.split] if self.split else None
        }
