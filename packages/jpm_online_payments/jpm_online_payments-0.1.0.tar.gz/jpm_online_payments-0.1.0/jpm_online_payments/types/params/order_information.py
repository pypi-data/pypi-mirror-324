import typing
import typing_extensions
import pydantic

from .order_item import OrderItem, _SerializerOrderItem


class OrderInformation(typing_extensions.TypedDict):
    """
    Partner's customer order information
    """

    merchant_url: typing_extensions.NotRequired[str]
    """
    A reference to a web resource on the internet specifying its location on a computer network and a mechanism for retrieving.
    """

    order_items: typing_extensions.NotRequired[typing.List[OrderItem]]
    """
    List of Order Items
    """

    payment_notes: typing_extensions.NotRequired[str]
    """
    Notes in the payment to specify the reason if the payment amount is not same as billing scheduled amount.
    """

    receipt_url: typing_extensions.NotRequired[str]
    """
    A reference to a web resource on the internet specifying its location on a computer network and a mechanism for retrieving.
    """

    terms_url: typing_extensions.NotRequired[str]
    """
    A reference to a web resource on the internet specifying its location on a computer network and a mechanism for retrieving.
    """


class _SerializerOrderInformation(pydantic.BaseModel):
    """
    Serializer for OrderInformation handling case conversions
    and file omissions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
        populate_by_name=True,
    )

    merchant_url: typing.Optional[str] = pydantic.Field(
        alias="merchantUrl", default=None
    )
    order_items: typing.Optional[typing.List[_SerializerOrderItem]] = pydantic.Field(
        alias="orderItems", default=None
    )
    payment_notes: typing.Optional[str] = pydantic.Field(
        alias="paymentNotes", default=None
    )
    receipt_url: typing.Optional[str] = pydantic.Field(alias="receiptUrl", default=None)
    terms_url: typing.Optional[str] = pydantic.Field(alias="termsUrl", default=None)
