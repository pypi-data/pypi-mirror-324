import typing
import pydantic

from .order_item import OrderItem


class OrderInformation(pydantic.BaseModel):
    """
    Partner's customer order information
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    merchant_url: typing.Optional[str] = pydantic.Field(
        alias="merchantUrl", default=None
    )
    """
    A reference to a web resource on the internet specifying its location on a computer network and a mechanism for retrieving.
    """
    order_items: typing.Optional[typing.List[OrderItem]] = pydantic.Field(
        alias="orderItems", default=None
    )
    """
    List of Order Items
    """
    payment_notes: typing.Optional[str] = pydantic.Field(
        alias="paymentNotes", default=None
    )
    """
    Notes in the payment to specify the reason if the payment amount is not same as billing scheduled amount.
    """
    receipt_url: typing.Optional[str] = pydantic.Field(alias="receiptUrl", default=None)
    """
    A reference to a web resource on the internet specifying its location on a computer network and a mechanism for retrieving.
    """
    terms_url: typing.Optional[str] = pydantic.Field(alias="termsUrl", default=None)
    """
    A reference to a web resource on the internet specifying its location on a computer network and a mechanism for retrieving.
    """
