import typing
import typing_extensions
import pydantic

from .authentication_value_response import AuthenticationValueResponse
from .three_ds import ThreeDs
from .token_authentication_result import TokenAuthenticationResult


class Authentication(pydantic.BaseModel):
    """
    The authentication object allows you to opt in to additional security features like 3-D Secure
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    sca_exemption_reason: typing.Optional[
        typing_extensions.Literal[
            "LOW_VALUE_PAYMENT",
            "MERCHANT_INITIATED_TRANSACTION",
            "RECURRING_PAYMENT",
            "SCA_DELEGATION",
            "SECURE_CORPORATE_PAYMENT",
            "TRANSACTION_RISK_ANALYSIS",
            "TRUSTED_MERCHANT",
        ]
    ] = pydantic.Field(alias="SCAExemptionReason", default=None)
    """
    Indicates the justification why a transaction does not have to meet Strong Customer Authentication (SCA) requirements.
    """
    authentication_id: typing.Optional[str] = pydantic.Field(
        alias="authenticationId", default=None
    )
    """
    Unique identifier for the card owner authentication provided by global authentication solution designed to make eCommerce transactions more secure and reduce fraud.
    """
    authentication_value_response: typing.Optional[AuthenticationValueResponse] = (
        pydantic.Field(alias="authenticationValueResponse", default=None)
    )
    """
    Returned when more information about authentication is received from the  network
    """
    electronic_commerce_indicator: typing.Optional[str] = pydantic.Field(
        alias="electronicCommerceIndicator", default=None
    )
    """
    Describes the Electronic Commerce Indicator used in cardholder authentication on a network token
    """
    three_ds: typing.Optional[ThreeDs] = pydantic.Field(alias="threeDS", default=None)
    """
    Contains information about payer authentication using 3-D Secure authentication
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
