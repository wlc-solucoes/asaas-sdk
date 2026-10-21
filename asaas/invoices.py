class Status:
    """Status de uma nota fiscal (NFS-e) no Asaas"""

    SCHEDULED = 'SCHEDULED'
    AUTHORIZED = 'AUTHORIZED'
    PROCESSING_CANCELLATION = 'PROCESSING_CANCELLATION'
    CANCELED = 'CANCELED'
    CANCELLATION_DENIED = 'CANCELLATION_DENIED'
    ERROR = 'ERROR'


class EffectiveDatePeriod:
    """Quando o Asaas emite a nota configurada numa assinatura"""

    ON_PAYMENT_CONFIRMATION = 'ON_PAYMENT_CONFIRMATION'
    ON_PAYMENT_DUE_DATE = 'ON_PAYMENT_DUE_DATE'
    BEFORE_PAYMENT_DUE_DATE = 'BEFORE_PAYMENT_DUE_DATE'
    ON_DUE_DATE_MONTH = 'ON_DUE_DATE_MONTH'
    ON_NEXT_MONTH = 'ON_NEXT_MONTH'


class Taxes:
    """Impostos da nota. Percentuais; `retainIss` indica ISS retido pelo tomador."""

    def __init__(
        self,
        retainIss: bool = False,
        iss: float = 0,
        pis: float = 0,
        cofins: float = 0,
        csll: float = 0,
        inss: float = 0,
        ir: float = 0,
        **extra
    ) -> None:
        self.retainIss = retainIss
        self.iss = iss
        self.pis = pis
        self.cofins = cofins
        self.csll = csll
        self.inss = inss
        self.ir = ir
        # Campos da reforma tributária e afins (nbsCode, taxSituationCode...) passam como estão.
        self.extra = extra

    def to_dict(self) -> dict:
        return {
            'retainIss': self.retainIss,
            'iss': self.iss,
            'pis': self.pis,
            'cofins': self.cofins,
            'csll': self.csll,
            'inss': self.inss,
            'ir': self.ir,
            **self.extra
        }
