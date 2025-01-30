import typing
import typing_extensions
import pydantic


class PaymentToken(pydantic.BaseModel):
    """
    Token Information for the payment transaction
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    response_status: typing.Optional[
        typing_extensions.Literal["DENIED", "ERROR", "SUCCESS"]
    ] = pydantic.Field(alias="responseStatus", default=None)
    """
    Indicates whether API request resulted in success, error, or denial.
    """
    token_number: typing.Optional[str] = pydantic.Field(
        alias="tokenNumber", default=None
    )
    """
    The token number is a secure surrogate value generated for an account number in a payment transaction. The token is substituted for the card number or primary account number (PAN), Demand Deposit Account (DDA) Number or other payment account and is used to process and identify transactions originating from that account.
    """
    token_provider: typing.Optional[
        typing_extensions.Literal["NETWORK", "SAFETECH"]
    ] = pydantic.Field(alias="tokenProvider", default=None)
    """
    The label given to a provider who creates the digital token for cards.
    """
    token_service_response_code: typing.Optional[str] = pydantic.Field(
        alias="tokenServiceResponseCode", default=None
    )
    """
    Short explanation of response Code
    """
    token_service_response_message: typing.Optional[str] = pydantic.Field(
        alias="tokenServiceResponseMessage", default=None
    )
    """
    Long explanation of response Message received from token service
    """
