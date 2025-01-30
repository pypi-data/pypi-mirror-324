import typing
import pydantic

from .token_authentication_result import TokenAuthenticationResult


class RefundAuthentication(pydantic.BaseModel):
    """
    The authentication object allows you to opt in to additional security features specific for refund
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    electronic_commerce_indicator: typing.Optional[str] = pydantic.Field(
        alias="electronicCommerceIndicator", default=None
    )
    """
    Describes the Electronic Commerce Indicator used in cardholder authentication on a network token
    """
    token_authentication_result: typing.Optional[TokenAuthenticationResult] = (
        pydantic.Field(alias="tokenAuthenticationResult", default=None)
    )
    """
    Returned when more information about token authentication is received from the network
    """
    token_authentication_value: typing.Optional[str] = pydantic.Field(
        alias="tokenAuthenticationValue", default=None
    )
    """
    Contains authentication value received from Payment Networks for network token transactions
    """
