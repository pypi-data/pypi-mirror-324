import typing
import typing_extensions
import pydantic


class PaymentCapture(pydantic.BaseModel):
    """
    Payment capture information for multi capture order
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    amount: typing.Optional[int] = pydantic.Field(alias="amount", default=None)
    """
    Total monetary value of the payment including all taxes and fees.
    """
    capture_id: typing.Optional[str] = pydantic.Field(alias="captureId", default=None)
    """
    Identifies a unique occurrence of a payment settlement request when the authorization is complete and the transaction is ready for settlement. The transaction can no longer be edited but can be voided.
    """
    capture_remaining_refundable_amount: typing.Optional[int] = pydantic.Field(
        alias="captureRemainingRefundableAmount", default=None
    )
    """
    Capture amount available to be refunded
    """
    transaction_status_code: typing.Optional[str] = pydantic.Field(
        alias="transactionStatusCode", default=None
    )
    """
    Indicates the status of payment transaction. For example, a typical transaction is authorized, then captured for clearing and settlement; "CLOSED" is when the transaction is ready for clearing and "COMPLETED" is when the transaction is sent to the payment network for clearing.
    """
    transaction_status_reason: typing.Optional[
        typing_extensions.Literal[
            "MANUAL_RISK_ACKNOWLEDGED",
            "MANUAL_RISK_REVIEW",
            "RISK_ACKNOWLEDGED",
            "RISK_APPROVED",
            "RISK_DENIED",
            "RISK_REVIEW",
            "VOIDED",
        ]
    ] = pydantic.Field(alias="transactionStatusReason", default=None)
    """
    Provides more context about the status of payment transaction (specifically, the review status of the payment capture information)
    """
