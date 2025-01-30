import typing
import typing_extensions
import pydantic


class PaymentAuth(pydantic.BaseModel):
    """
    Authorization request information for multi capture order
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    amount: typing.Optional[int] = pydantic.Field(alias="amount", default=None)
    """
    Total monetary value of the payment including all taxes and fees.
    """
    authorization_id: typing.Optional[str] = pydantic.Field(
        alias="authorizationId", default=None
    )
    """
    Identifies a unique occurrence of an authorization that is associated with a purchase of goods and/or services. More than one authorization can exist for a purchase, as an example in fuel and hotel services a merchant can send multiple authorization requests when the exact amount is unknown until completion of the sale.
    """
    authorization_type: typing.Optional[
        typing_extensions.Literal["INCREMENTAL", "INITIAL", "REAUTH"]
    ] = pydantic.Field(alias="authorizationType", default=None)
    """
    Specifies the type of authorization requested.
    """
    transaction_status_code: typing.Optional[str] = pydantic.Field(
        alias="transactionStatusCode", default=None
    )
    """
    Indicates the status of payment transaction. For example, a typical transaction is authorized, then captured for clearing and settlement; "CLOSED" is when the transaction is ready for clearing and "COMPLETED" is when the transaction is sent to the payment network for clearing.
    """
