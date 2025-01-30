import typing
import typing_extensions
import pydantic


class TokenAuthenticationResult(typing_extensions.TypedDict):
    """
    Returned when more information about token authentication is received from the network
    """

    code_field: typing_extensions.NotRequired[str]
    """
    Token result code
    """

    message: typing_extensions.NotRequired[str]
    """
    Token result message
    """


class _SerializerTokenAuthenticationResult(pydantic.BaseModel):
    """
    Serializer for TokenAuthenticationResult handling case conversions
    and file omissions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
        populate_by_name=True,
    )

    code_field: typing.Optional[str] = pydantic.Field(alias="code", default=None)
    message: typing.Optional[str] = pydantic.Field(alias="message", default=None)
