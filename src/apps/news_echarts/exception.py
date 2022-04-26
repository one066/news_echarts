from extension.flask.exceptions import APIException


class UserEmailAlreadyExist(APIException):
    error_type = "Login failed"
    error_message = "User email already exist"


class UserNickNameAlreadyExist(APIException):
    error_type = "Login failed"
    error_message = "User email already exist"


class WrongPassword(APIException):
    error_type = "Login failed"
    error_message = "Wrong password"


class WrongVerificationCode(APIException):
    error_type = "Login failed"
    error_message = "Wrong verification code"


class VerificationCodeExpired(APIException):
    error_type = "Login failed"
    error_message = "Verification code expired"


class NotMessage(APIException):
    error_type = "Chat"
    error_message = "Not more message"
