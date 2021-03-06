class ErrorCodes:
    # general error
    unknown_internal_server_error = 9999

    # code 10xx server error
    redis_error = 1002
    mysql_error = 1003
    email_error = 1004

    # code 11xx application validation error
    validation_error = 1100
    already_final_submitted = 1101
    any_application_submitted_yet = 1102

    # code 12xx auth error
    user_not_found = 1200
    token_expired = 1201
    invalid_token = 1202

    # code 13xx signup error
    invalid_signup_info = 1300
    user_already_exists = 1301
    signup_already_requested = 1302
    invalid_verification_key = 1303


class ErrorDescriptions:
    # specific error description
    ERR_SERVER = (
        "Our service is currently unavailable. Please try again later."
    )
    ERR_DATABASE = "Something went wrong."
    ERR_EMAIL = "Email error occurred."

    ERR_APPLICATION_PATCH_VALIDATION = "Invalid application submitted."
    ERR_APPLICATION_FINAL_SUBMIT_VALIDATION = (
        "Please fill out all column before final submit."
    )
    ERR_ALREADY_FINAL_SUBMITTED = (
        "Final submitted application can't be edited."
    )
    ERR_ANY_APPLICATION_SUBMITTED_YET = "Any application submitted yet."
    ERR_WRONG_IMAGE_DATA = "Invalid image. Only allow png, jpeg, jpg, jp2, j2c"
    ERR_IMAGE_NOT_FOUND = "No image data yet."

    ERR_USER_NOT_FOUND = "Login information is incorrect"
    ERR_TOKEN_ERROR = "Please login again"

    ERR_INVALID_SIGNUP_INFO = "Invalid signup request"
    ERR_USER_ALREADY_EXISTS = "Email is in use."
    ERR_SIGNUP_ALREADY_REQUESTED = "Signup verification email already sent"
    ERR_INVALID_VERIFICATION_KEY = "Invalid or expired verification key"


error_codes = ErrorCodes()
descriptions = ErrorDescriptions()
