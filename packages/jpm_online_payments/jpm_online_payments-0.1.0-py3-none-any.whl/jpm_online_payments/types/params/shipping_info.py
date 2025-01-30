import typing
import typing_extensions
import pydantic


class ShippingInfo(typing_extensions.TypedDict):
    """
    Partner's Shipping Information
    """

    expected_merchant_product_delivery_date: typing_extensions.NotRequired[str]
    """
    Designates the year, month and day reported by merchant when items or services are expected to be delivered.
    """

    shipping_carrier_name: typing_extensions.NotRequired[str]
    """
    The label given to the external vendor who provides delivery service to the merchant to deliver products to consumers.
    """


class _SerializerShippingInfo(pydantic.BaseModel):
    """
    Serializer for ShippingInfo handling case conversions
    and file omissions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
        populate_by_name=True,
    )

    expected_merchant_product_delivery_date: typing.Optional[str] = pydantic.Field(
        alias="expectedMerchantProductDeliveryDate", default=None
    )
    shipping_carrier_name: typing.Optional[str] = pydantic.Field(
        alias="shippingCarrierName", default=None
    )
