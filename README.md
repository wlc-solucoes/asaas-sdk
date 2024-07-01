# Asaas SDK
SDK não oficial para comunicação com a API do Asaas seguindo a documentação oficial em: https://docs.asaas.com/

## Instalação
```pip install asaas-sdk-wlc```

## Como utilizar

```py
from asaas import Asaas

asaas = Asaas(
    api_key=ACCESS_TOKEN, 
    production=False
)
```

## Customers (clientes)

```py
# Listar clientes
list_of_customers = asaas.customers.list(
    name='John Doe',
    email='johndoe@email.com',
    cpfCnpj='43883912042',
    groupName='WLC',
    externalReference='123456',
    offset=0,
    limit=10
)

# Criar novo cliente
customer = asaas.customers.create(
    name='John Doe',
    cpfCnpj='43883912042',
    email='johndoe@email.com',
    phone='82999999999',
    mobilePhone='82999999999',
    address='R. José Maia Gomes',
    addressNumber='258',
    complement='',
    province='Jatiúca',
    postalCode='57036170',
    externalReference='123456',
    notificationDisabled=False,
    additionalEmails=None,
    municipalInscription=None,
    stateInscription=None,
    observations=None,
    groupName=None,
    company=None
)

# Recuperar um único cliente

customer = asaas.customers.retrieve(
    customer_id='cus_000006070645'
)

# Atualizar cliente

customer = asaas.customers.update(
    customer_id='cus_000006070645'
    name='John Doe',
    cpfCnpj='43883912042',
    email='johndoe@email.com',
    phone='82999999999',
    mobilePhone='82999999999',
    address='R. José Maia Gomes',
    addressNumber='258',
    complement='',
    province='Jatiúca',
    postalCode='57036170',
    externalReference='123456',
    notificationDisabled=False,
    additionalEmails=None,
    municipalInscription=None,
    stateInscription=None,
    observations=None,
    groupName=None,
    company=None
)

# Excluir cliente

asaas.customers.delete(customer_id='cus_000006070645')

# Restaurar cliente

customer = asaas.customers.restore(customer_id='cus_000006070645')

```

## Payments (Cobranças)

```py
from asaas import payments

# Listar cobranças

list_of_payments = asaas.payments.list(
    customer='cus_000006070645',
    customerGroupName=None,
    billingType=payments.BillingType.PIX,
    status=payments.Status.PENDING,
    subscription=None,
    installment=None,
    externalReference=None,
    paymentDate=None,
    invoiceStatus=None,
    estimatedCreditDate=None,
    pixQrCodeId=None,
    antipated=True,
    dateCreatedGreaterThanOrEqual=None,
    dateCreatedLessThanOrEqual=None,
    paymentDateGreaterThanOrEqual=None,
    paymentDateLessThanOrEqual=None,
    estimatedCreditDateGreaterThanOrEqual=None,
    estimatedCreditDateLessThanOrEqual=None,
    dueDateGreaterThanOrEqual=None,
    dueDateLessThanOrEqual=None,
    user=None,
    offset=0,
    limit=10
)

# Criar cobrança

discount = payments.Discount(
    value=5,
    dueDateLimitDays=3,
    type=payments.Discount.Type.PERCENTAGE
)

interest = payments.Interest(
    value=10
)

fine = payments.Fine(
    value=1.5,
    type=payments.Fine.Type.PERCENTAGE
)

split_1 = payments.Split(
    walletId=WALLET_ID_1,
    fixedValue=None,
    percentageValue=50,
    totalFixedValue=None
)

split_2 = payments.Split(
    walletId=WALLET_ID_2,
    fixedValue=None,
    percentageValue=50,
    totalFixedValue=None
)

callback = payments.Callback(
    sucessUrl=URL,
    autoRedirect=True
)

payment = asaas.payments.create(
    customer='cus_000006070645',
    value=100,
    dueDate='2024-12-31',
    billingType=payments.BillingType.UNDEFINED,
    description=None,
    daysAfterDueDateToRegistrationCancellation=None,
    externalReference='123456',
    installmentCount=None,
    totalValue=None,
    installmentValue=None,
    discount=discount,
    interest=interest,
    fine=fine,
    split=[split_1, split_2],
    callback=callback
)

# Recuperar uma única cobrança

payments = asaas.payments.retrieve(
    payment_id='pay_7po81e74ptiid0re'
)

# Atualizar cobrança

payment = asaas.payments.update(
    payment_id='pay_7po81e74ptiid0re',
    value=100,
    dueDate='2024-12-31',
    billingType=payments.BillingType.UNDEFINED,
    description=None,
    daysAfterDueDateToRegistrationCancellation=None,
    externalReference='123456',
    installmentCount=None,
    totalValue=None,
    installmentValue=None,
    discount=discount,
    interest=interest,
    fine=fine,
    postalService=False,
    split=[split_1, split_2],
    callback=callback
)

# Excluir cobrança

asaas.payments.delete(
    payment_id='pay_7po81e74ptiid0re'
)

# Restaurar uma cobrança
payment = asaas.payments.restore(
    payment_id='pay_7po81e74ptiid0re'
)

# Estornar cobrança
payment = asaas.payments.refund(
    payment_id='pay_7po81e74ptiid0re'
    value=50,
    description=None
)

```