import typing
import pydantic


class PaymentRefund(pydantic.BaseModel):
    """
    Payment refund information for multi capture order
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    amount: typing.Optional[int] = pydantic.Field(alias="amount", default=None)
    """
    Total monetary value of the payment including all taxes and fees.
    """
    refund_id: typing.Optional[str] = pydantic.Field(alias="refundId", default=None)
    """
    Identifies a unique occurrence of a payment settlement request when the authorization is complete and the transaction is ready for settlement. The transaction can no longer be edited but can be voided.
    """
    transaction_status_code: typing.Optional[str] = pydantic.Field(
        alias="transactionStatusCode", default=None
    )
    """
    Indicates the status of payment transaction. For example, a typical transaction is authorized, then captured for clearing and settlement; "CLOSED" is when the transaction is ready for clearing and "COMPLETED" is when the transaction is sent to the payment network for clearing.
    """
