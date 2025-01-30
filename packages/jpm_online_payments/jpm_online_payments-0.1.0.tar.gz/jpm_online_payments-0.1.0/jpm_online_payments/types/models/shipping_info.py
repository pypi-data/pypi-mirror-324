import typing
import pydantic


class ShippingInfo(pydantic.BaseModel):
    """
    Partner's Shipping Information
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    expected_merchant_product_delivery_date: typing.Optional[str] = pydantic.Field(
        alias="expectedMerchantProductDeliveryDate", default=None
    )
    """
    Designates the year, month and day reported by merchant when items or services are expected to be delivered.
    """
    shipping_carrier_name: typing.Optional[str] = pydantic.Field(
        alias="shippingCarrierName", default=None
    )
    """
    The label given to the external vendor who provides delivery service to the merchant to deliver products to consumers.
    """
