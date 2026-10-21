import json
import unittest
from datetime import date

from asaas import Asaas, invoices
from asaas.exceptions import AsaasError, AuthenticationAsaas, InvalidCustomerAsaas, NotFoundAsaas


class FakeResponse:

    def __init__(self, status_code=200, body=None, content=None, url='https://api-sandbox.asaas.com/v3/x'):
        self.status_code = status_code
        self._body = body
        self.content = content if content is not None else json.dumps(body or {}).encode()
        self.url = url

    def json(self):
        if self._body is None:
            raise ValueError('sem json')
        return self._body

    def raise_for_status(self):
        if self.status_code >= 400:
            from requests.exceptions import HTTPError
            raise HTTPError(f'{self.status_code}')


class FakeSession:

    def __init__(self, *responses):
        self.responses = list(responses)
        self.calls = []

    def request(self, method, url, **kwargs):
        self.calls.append((method, url, kwargs))
        return self.responses.pop(0)


PAYMENT = {
    'id': 'pay_1', 'customer': 'cus_1', 'dateCreated': '2026-10-19', 'dueDate': '2026-11-10',
    'value': 100.0, 'status': 'PENDING', 'billingType': 'BOLETO', 'campoNovo': 'ignorado'
}


class ClientTests(unittest.TestCase):

    def make(self, *responses):
        session = FakeSession(*responses)
        return Asaas('chave', production=False, user_agent='oegadv', session=session), session

    def test_headers_user_agent_and_timeout(self):
        asaas, session = self.make(FakeResponse(body=PAYMENT))
        asaas.payments.retrieve('pay_1')
        method, url, kwargs = session.calls[0]
        self.assertEqual(method, 'GET')
        self.assertEqual(url, 'https://api-sandbox.asaas.com/v3/payments/pay_1')
        self.assertEqual(kwargs['headers']['User-Agent'], 'oegadv')
        self.assertEqual(kwargs['headers']['access_token'], 'chave')
        self.assertEqual(kwargs['timeout'], 30)
        self.assertNotIn('json', kwargs)

    def test_post_without_body_sends_empty_json(self):
        asaas, session = self.make(FakeResponse(body=PAYMENT))
        asaas.payments.restore('pay_1')
        self.assertEqual(session.calls[0][2]['json'], {})

    def test_identification_field(self):
        asaas, session = self.make(FakeResponse(body={'identificationField': '2379', 'nossoNumero': '6', 'barCode': '237'}))
        result = asaas.payments.identification_field('pay_1')
        self.assertEqual(result.identificationField, '2379')
        self.assertTrue(session.calls[0][1].endswith('/payments/pay_1/identificationField'))

    def test_receive_in_cash(self):
        asaas, session = self.make(FakeResponse(body={**PAYMENT, 'status': 'RECEIVED_IN_CASH'}))
        payment = asaas.payments.receive_in_cash('pay_1', paymentDate=date(2026, 10, 19), value=100)
        self.assertEqual(payment.status, 'RECEIVED_IN_CASH')
        self.assertEqual(session.calls[0][2]['json'], {'paymentDate': '2026-10-19', 'value': 100})

    def test_installment_create_and_payment_book(self):
        asaas, session = self.make(
            FakeResponse(body={'id': 'ins_1', 'installmentCount': 3}),
            FakeResponse(body={'data': [{**PAYMENT, 'id': 'pay_3', 'installmentNumber': 2},
                                        {**PAYMENT, 'id': 'pay_2', 'installmentNumber': 1}]}),
            FakeResponse(content=b'%PDF-1.4', body=None),
        )
        installment = asaas.installments.create(
            customer='cus_1', installmentCount=3, dueDate=date(2026, 11, 10), value=100
        )
        self.assertEqual(installment.id, 'ins_1')
        body = session.calls[0][2]['json']
        self.assertEqual(body['value'], 100)
        self.assertEqual(body['billingType'], 'BOLETO')
        payments = asaas.installments.list_payments('ins_1')
        self.assertEqual([p.id for p in payments], ['pay_2', 'pay_3'])
        self.assertEqual(asaas.installments.payment_book('ins_1'), b'%PDF-1.4')

    def test_installment_requires_value_or_total(self):
        asaas, _ = self.make()
        with self.assertRaises(ValueError):
            asaas.installments.create(customer='c', installmentCount=2, dueDate=date(2026, 1, 1))
        with self.assertRaises(ValueError):
            asaas.installments.create(customer='c', installmentCount=1, dueDate=date(2026, 1, 1), value=1)

    def test_invoice_schedule_and_authorize(self):
        asaas, session = self.make(
            FakeResponse(body={'id': 'inv_1', 'status': 'SCHEDULED'}),
            FakeResponse(body={'id': 'inv_1', 'status': 'SCHEDULED'}),
        )
        invoice = asaas.invoices.schedule(
            serviceDescription='Honorários', value=100, effectiveDate=date(2026, 10, 19),
            taxes=invoices.Taxes(iss=2), payment='pay_1', municipalServiceCode='17.14',
            externalReference='ref1'
        )
        self.assertEqual(invoice.status, 'SCHEDULED')
        body = session.calls[0][2]['json']
        self.assertEqual(body['municipalServiceName'], '17.14')
        self.assertEqual(body['taxes']['iss'], 2)
        self.assertEqual(body['externalReference'], 'ref1')
        asaas.invoices.authorize('inv_1')
        self.assertTrue(session.calls[1][1].endswith('/invoices/inv_1/authorize'))

    def test_fiscal_info_is_multipart(self):
        asaas, session = self.make(FakeResponse(body={'object': 'customerFiscalInfo', 'certificateSent': True}))
        asaas.fiscal_info.save(email='a@b.com', simplesNacional=True, certificateFile=b'pfx', certificatePassword='x')
        kwargs = session.calls[0][2]
        self.assertIn('files', kwargs)
        self.assertEqual(kwargs['data']['simplesNacional'], 'true')
        self.assertNotIn('json', kwargs)

    def test_errors(self):
        asaas, _ = self.make(
            FakeResponse(400, {'errors': [{'code': 'invalid_customer', 'description': 'Cliente inválido'}]}),
            FakeResponse(401, {'errors': [{'code': 'invalid_environment', 'description': 'x'}]}),
            FakeResponse(404, {}),
            FakeResponse(500, None, content=b'erro'),
        )
        with self.assertRaises(InvalidCustomerAsaas) as ctx:
            asaas.payments.retrieve('x')
        self.assertEqual(ctx.exception.code, 'invalid_customer')
        self.assertEqual(ctx.exception.message, 'Cliente inválido')
        with self.assertRaises(AuthenticationAsaas):
            asaas.payments.retrieve('x')
        with self.assertRaises(NotFoundAsaas):
            asaas.payments.retrieve('x')
        with self.assertRaises(AsaasError):
            asaas.payments.retrieve('x')

    def test_webhook_list_page(self):
        asaas, _ = self.make(FakeResponse(body={'data': [{'id': 'wh_1', 'url': 'u'}], 'hasMore': False, 'totalCount': 1}))
        hooks = asaas.webhooks.list()
        self.assertEqual(hooks[0].id, 'wh_1')
        self.assertEqual(hooks.total_count, 1)


if __name__ == '__main__':
    unittest.main()
