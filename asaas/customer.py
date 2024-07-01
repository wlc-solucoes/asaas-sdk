from typing import Optional
from datetime import date


class Customer:
    def __init__(
        self,
        id: str,
        dateCreated: date,
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
        **kwargs
    ) -> None:

        self.id = id
        self.dateCreated = dateCreated if type(
            dateCreated) == date else date.fromisoformat(dateCreated)
        self.name = name
        self.cpfCnpj = cpfCnpj
        self.email = email
        self.phone = phone
        self.mobilePhone = mobilePhone
        self.address = address
        self.addressNumber = addressNumber
        self.complement = complement
        self.province = province
        self.postalCode = postalCode
        self.externalReference = externalReference
        self.notificationDisabled = notificationDisabled
        self.additionalEmails = additionalEmails
        self.municipalInscription = municipalInscription
        self.stateInscription = stateInscription
        self.observations = observations

    def to_dict(self):
        return {
            'id': self.id,
            'dateCreated': self.dateCreated.strftime('%Y-%m-%d'),
            'name': self.name,
            'cpfCnpj': self.cpfCnpj,
            'email': self.email,
            'phone': self.phone,
            'mobilePhone': self.mobilePhone,
            'address': self.address,
            'addressNumber': self.addressNumber,
            'complement': self.complement,
            'province': self.province,
            'postalCode': self.postalCode,
            'externalReference': self.externalReference,
            'notificationDisabled': self.notificationDisabled,
            'additionalEmails': self.additionalEmails,
            'municipalInscription': self.municipalInscription,
            'stateInscription': self.stateInscription,
            'observations': self.observations
        }
