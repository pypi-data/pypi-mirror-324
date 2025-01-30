import typing
import typing_extensions
import pydantic

from .authentication_value_response import (
    AuthenticationValueResponse,
    _SerializerAuthenticationValueResponse,
)
from .three_ds import ThreeDs, _SerializerThreeDs
from .token_authentication_result import (
    TokenAuthenticationResult,
    _SerializerTokenAuthenticationResult,
)


class Authentication(typing_extensions.TypedDict):
    """
    The authentication object allows you to opt in to additional security features like 3-D Secure
    """

    sca_exemption_reason: typing_extensions.NotRequired[
        typing_extensions.Literal[
            "LOW_VALUE_PAYMENT",
            "MERCHANT_INITIATED_TRANSACTION",
            "RECURRING_PAYMENT",
            "SCA_DELEGATION",
            "SECURE_CORPORATE_PAYMENT",
            "TRANSACTION_RISK_ANALYSIS",
            "TRUSTED_MERCHANT",
        ]
    ]
    """
    Indicates the justification why a transaction does not have to meet Strong Customer Authentication (SCA) requirements.
    """

    authentication_id: typing_extensions.NotRequired[str]
    """
    Unique identifier for the card owner authentication provided by global authentication solution designed to make eCommerce transactions more secure and reduce fraud.
    """

    authentication_value_response: typing_extensions.NotRequired[
        AuthenticationValueResponse
    ]
    """
    Returned when more information about authentication is received from the  network
    """

    electronic_commerce_indicator: typing_extensions.NotRequired[str]
    """
    Describes the Electronic Commerce Indicator used in cardholder authentication on a network token
    """

    three_ds: typing_extensions.NotRequired[ThreeDs]
    """
    Contains information about payer authentication using 3-D Secure authentication
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


class _SerializerAuthentication(pydantic.BaseModel):
    """
    Serializer for Authentication handling case conversions
    and file omissions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
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
    authentication_id: typing.Optional[str] = pydantic.Field(
        alias="authenticationId", default=None
    )
    authentication_value_response: typing.Optional[
        _SerializerAuthenticationValueResponse
    ] = pydantic.Field(alias="authenticationValueResponse", default=None)
    electronic_commerce_indicator: typing.Optional[str] = pydantic.Field(
        alias="electronicCommerceIndicator", default=None
    )
    three_ds: typing.Optional[_SerializerThreeDs] = pydantic.Field(
        alias="threeDS", default=None
    )
    token_authentication_result: typing.Optional[
        _SerializerTokenAuthenticationResult
    ] = pydantic.Field(alias="tokenAuthenticationResult", default=None)
    token_authentication_value: typing.Optional[str] = pydantic.Field(
        alias="tokenAuthenticationValue", default=None
    )
