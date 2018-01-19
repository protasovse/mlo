class ControlledException(Exception):
    code = 'error'
    request_status = 500

    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self.fields = []
        self.code = kwargs.get('code', 'error')
        field = kwargs.get('field', False)
        if field:
            self.fields.append(field)
        self.request_status = int(kwargs.get('request_status', 500))


class BackendPublicException(ControlledException):
    pass


class ApiPublicException(ControlledException):
    pass


class ApiException(ControlledException):
    pass