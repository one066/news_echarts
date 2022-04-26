class APIException(Exception):
    """异常处理
    """
    error_type = 'api_error'
    error_message = 'api_error'

    def __init__(self, error_type=None, error_message=None):
        if error_type is not None:
            self.error_type = error_type
        if error_message is not None:
            self.error_message = error_message

    def __repr__(self):
        return '<{} {}: {}>'.format(
            self.__class__, self.error_type, self.error_message
        )


class TokenFailed(APIException):
    error_type = 'Token failed'
    error_message = 'Token failed'
