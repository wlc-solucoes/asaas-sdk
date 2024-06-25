from json import JSONEncoder


class AsaasEncoder(JSONEncoder):
    def default(self, object):
        try:
            return object.to_dict()
        except AttributeError:
            return super().default(object)
