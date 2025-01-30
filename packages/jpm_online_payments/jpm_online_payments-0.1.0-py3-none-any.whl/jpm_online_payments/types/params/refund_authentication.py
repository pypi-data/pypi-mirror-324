import typing
import typing_extensions
import pydantic

from .token_authentication_result import (
    TokenAuthenticationResult,
    _SerializerTokenAuthenticationResult,
)


class RefundAuthentication(typing_extensions.TypedDict):
    """
    The authentication object allows you to opt in to additional security features specific for refund
    """

    electronic_commerce_indicator: typing_extensions.NotRequired[str]
    """
    Describes the Electronic Commerce Indicator used in cardholder authentication on a network token
    """

    token_authentication_result: typing_extensions.NotRequired[
        TokenAuthenticationResult
    ]
    """
    Returned when more information about token authentication is received from the network
    """

    token_authentication_value: typing_extensions.NotRequired[str]
    """
    Contains authentication value received from Payment Networks for network token transactions
    """


class _SerializerRefundAuthentication(pydantic.BaseModel):
    """
    Serializer for RefundAuthentication handling case conversions
    and file omissions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
        populate_by_name=True,
    )

    electronic_commerce_indicator: typing.Optional[str] = pydantic.Field(
        alias="electronicCommerceIndicator", default=None
    )
    token_authentication_result: typing.Optional[
        _SerializerTokenAuthenticationResult
    ] = pydantic.Field(alias="tokenAuthenticationResult", default=None)
    token_authentication_value: typing.Optional[str] = pydantic.Field(
        alias="tokenAuthenticationValue", default=None
    )
