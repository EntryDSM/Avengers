from marshmallow import Schema, validate
from marshmallow.fields import Email, String


class SignUpRequestSchema(Schema):
    email = Email(required=True, allow_none=False)
    password = String(
        required=True,
        allow_none=False,
        validate=validate.Length(min=8, max=64),
    )


class LoginRequestSchema(SignUpRequestSchema):
    """Login Schema"""

