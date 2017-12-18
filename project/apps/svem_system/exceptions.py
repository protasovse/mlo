class ControlledException(Exception):
    code = 'error'
    request_status = 500

    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self.code = kwargs.get('code', 'error')
        self.request_status = int(kwargs.get('request_status', 500))


class BackendPublicException(ControlledException):
    pass


class ApiPublicException(ControlledException):
    pass


class ApiException(ControlledException):
    pass