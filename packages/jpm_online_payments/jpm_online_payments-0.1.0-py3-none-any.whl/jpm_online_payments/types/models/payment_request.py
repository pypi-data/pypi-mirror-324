import typing
import typing_extensions
import pydantic

from .payment_auth import PaymentAuth
from .payment_capture import PaymentCapture
from .payment_refund import PaymentRefund


class PaymentRequest(pydantic.BaseModel):
    """
    Payment request information for multi capture order
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    authorizations: typing.Optional[typing.List[PaymentAuth]] = pydantic.Field(
        alias="authorizations", default=None
    )
    """
    List of payment authorization information
    """
    captures: typing.Optional[typing.List[PaymentCapture]] = pydantic.Field(
        alias="captures", default=None
    )
    """
    List of payment capture information
    """
    payment_request_id: typing.Optional[str] = pydantic.Field(
        alias="paymentRequestId", default=None
    )
    """
    Identifies a unique occurrence of an payment processing request from merchant that is associated with a purchase of goods and/or services. A payment request consist of authorization, captures and refunds.
    """
    payment_request_status: typing.Optional[
        typing_extensions.Literal["CANCELLED", "CLOSED", "OPEN", "PENDING"]
    ] = pydantic.Field(alias="paymentRequestStatus", default=None)
    """
    Indicates the status of payment request from the merchant. A payment request consists of authorization, capture and refund.
    """
    refunds: typing.Optional[typing.List[PaymentRefund]] = pydantic.Field(
        alias="refunds", default=None
    )
    """
    List of payment refund information
    """
