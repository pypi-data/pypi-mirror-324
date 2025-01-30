import typing
import typing_extensions
import pydantic


class AuthenticationValueResponse(typing_extensions.TypedDict):
    """
    Returned when more information about authentication is received from the  network
    """

    code_field: typing_extensions.NotRequired[str]
    """
    3-D Secure authentication response code
    """

    message: typing_extensions.NotRequired[str]
    """
    3-D Secure authentication response message
    """


class _SerializerAuthenticationValueResponse(pydantic.BaseModel):
    """
    Serializer for AuthenticationValueResponse handling case conversions
    and file omissions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
        populate_by_name=True,
    )

    code_field: typing.Optional[str] = pydantic.Field(alias="code", default=None)
    message: typing.Optional[str] = pydantic.Field(alias="message", default=None)
