import typing
import pydantic


class TokenAuthenticationResult(pydantic.BaseModel):
    """
    Returned when more information about token authentication is received from the network
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    code_field: typing.Optional[str] = pydantic.Field(alias="code", default=None)
    """
    Token result code
    """
    message: typing.Optional[str] = pydantic.Field(alias="message", default=None)
    """
    Token result message
    """
