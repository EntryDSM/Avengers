class ErrorCodes:
    # general errors
    unknown_internal_server_error = 9999

    redis_error = 1002
    mysql_error = 1003

    def __getattribute__(self, attribute):
        return attribute


class ErrorDescriptions:
    # specific error description
    ERR_SERVER = (
        "Our service is currently unavailable. Please try again later."
    )
    ERR_DATABASE = "Something went wrong."

    def __getattribute__(self, attribute):
        return attribute


error_codes = ErrorCodes()
descriptions = ErrorDescriptions()
