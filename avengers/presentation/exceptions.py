from sanic.exceptions import SanicException, add_status_code

from avengers.presentation.errors import descriptions, error_codes


@add_status_code(503)
class AvengersException(SanicException):
    error_code = error_codes.unknown_internal_server_error
    description = descriptions.ERR_SERVER


@add_status_code(503)
class RedisOperationError(AvengersException):
    error_code = error_codes.redis_error
    description = descriptions.ERR_DATABASE


@add_status_code(503)
class MySQLOperationError(AvengersException):
    error_code = error_codes.mysql_error
    description = descriptions.ERR_DATABASE


@add_status_code(400)
class InvalidApplication(AvengersException):
    error_code = error_codes.validation_error
    description = descriptions.ERR_APPLICATION_PATCH_VALIDATION


@add_status_code(400)
class FinalValidationFailed(InvalidApplication):
    description = descriptions.ERR_APPLICATION_FINAL_SUBMIT_VALIDATION


@add_status_code(409)
class AlreadyFinalSubmitted(AvengersException):
    error_code = error_codes.already_final_submitted
    description = descriptions.ERR_ALREADY_FINAL_SUBMITTED


@add_status_code(404)
class ApplicationNotFound(AvengersException):
    error_code = error_codes.any_application_submitted_yet
    descriptions = descriptions.ERR_ANY_APPLICATION_SUBMITTED_YET


@add_status_code(403)
class UserNotFound(AvengersException):
    error_code = error_codes.user_not_found
    description = descriptions.ERR_USER_NOT_FOUND


@add_status_code(401)
class TokenError(AvengersException):
    error_code = error_codes.invalid_token
    description = descriptions.ERR_TOKEN_ERROR


@add_status_code(401)
class TokenExpired(TokenError):
    error_code = error_codes.token_expired


@add_status_code(400)
class InvalidSignupInfo(AvengersException):
    error_code = error_codes.invalid_signup_info
    description = descriptions.ERR_INVALID_SIGNUP_INFO


@add_status_code(409)
class UserAlreadyExists(AvengersException):
    error_code = error_codes.user_already_exists
    description = descriptions.ERR_USER_ALREADY_EXISTS


@add_status_code(409)
class SignupAlreadyRequested(AvengersException):
    error_code = error_codes.signup_already_requested
    description = descriptions.ERR_SIGNUP_ALREADY_REQUESTED


@add_status_code(400)
class InvalidVerificationKey(AvengersException):
    error_code = error_codes.invalid_verification_key
    description = descriptions.ERR_INVALID_VERIFICATION_KEY
