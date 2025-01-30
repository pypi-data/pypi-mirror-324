import typing
import pydantic


class AuthenticationValueResponse(pydantic.BaseModel):
    """
    Returned when more information about authentication is received from the  network
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    code_field: typing.Optional[str] = pydantic.Field(alias="code", default=None)
    """
    3-D Secure authentication response code
    """
    message: typing.Optional[str] = pydantic.Field(alias="message", default=None)
    """
    3-D Secure authentication response message
    """
