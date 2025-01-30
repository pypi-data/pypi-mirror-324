import typing
import typing_extensions
import pydantic


class PaymentToken(typing_extensions.TypedDict):
    """
    Token Information for the payment transaction
    """

    response_status: typing_extensions.NotRequired[
        typing_extensions.Literal["DENIED", "ERROR", "SUCCESS"]
    ]
    """
    Indicates whether API request resulted in success, error, or denial.
    """

    token_number: typing_extensions.NotRequired[str]
    """
    The token number is a secure surrogate value generated for an account number in a payment transaction. The token is substituted for the card number or primary account number (PAN), Demand Deposit Account (DDA) Number or other payment account and is used to process and identify transactions originating from that account.
    """

    token_provider: typing_extensions.NotRequired[
        typing_extensions.Literal["NETWORK", "SAFETECH"]
    ]
    """
    The label given to a provider who creates the digital token for cards.
    """

    token_service_response_code: typing_extensions.NotRequired[str]
    """
    Short explanation of response Code
    """

    token_service_response_message: typing_extensions.NotRequired[str]
    """
    Long explanation of response Message received from token service
    """


class _SerializerPaymentToken(pydantic.BaseModel):
    """
    Serializer for PaymentToken handling case conversions
    and file omissions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
        populate_by_name=True,
    )

    response_status: typing.Optional[
        typing_extensions.Literal["DENIED", "ERROR", "SUCCESS"]
    ] = pydantic.Field(alias="responseStatus", default=None)
    token_number: typing.Optional[str] = pydantic.Field(
        alias="tokenNumber", default=None
    )
    token_provider: typing.Optional[
        typing_extensions.Literal["NETWORK", "SAFETECH"]
    ] = pydantic.Field(alias="tokenProvider", default=None)
    token_service_response_code: typing.Optional[str] = pydantic.Field(
        alias="tokenServiceResponseCode", default=None
    )
    token_service_response_message: typing.Optional[str] = pydantic.Field(
        alias="tokenServiceResponseMessage", default=None
    )
