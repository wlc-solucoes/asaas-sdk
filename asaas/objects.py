class AsaasObject(dict):
    """Resposta do Asaas como dicionário com acesso por atributo.

    Usado pelos recursos novos (parcelamentos, notas, fiscalInfo, webhooks): campo novo que o Asaas
    acrescentar na resposta não quebra o SDK, ao contrário de um construtor com argumentos fixos.
    """

    def __getattr__(self, name):
        try:
            value = self[name]
        except KeyError as error:
            raise AttributeError(name) from error
        return AsaasObject.wrap(value)

    @staticmethod
    def wrap(value):
        if isinstance(value, dict) and not isinstance(value, AsaasObject):
            return AsaasObject(value)
        if isinstance(value, list):
            return [AsaasObject.wrap(item) for item in value]
        return value


class AsaasList(list):
    """Página de uma listagem do Asaas (`data`) com `has_more`, `total_count`, `limit` e `offset`."""

    def __init__(self, envelope: dict):
        super().__init__(AsaasObject.wrap(item) for item in envelope.get('data', []))
        self.has_more = envelope.get('hasMore', False)
        self.total_count = envelope.get('totalCount', len(self))
        self.limit = envelope.get('limit')
        self.offset = envelope.get('offset')
