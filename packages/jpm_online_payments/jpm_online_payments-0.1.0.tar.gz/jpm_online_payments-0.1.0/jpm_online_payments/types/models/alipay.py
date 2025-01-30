import typing
import pydantic

from .redirected_payment import RedirectedPayment


class Alipay(pydantic.BaseModel):
    """
    Alipay payment method is a single-use payment method where customers are required to authenticate their payment.
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    completion_time: typing.Optional[str] = pydantic.Field(
        alias="completionTime", default=None
    )
    """
    Provides a timestamp (UTC). Designates the hour (hh), minute (mm), seconds (ss) and date (if timestamp) or year (YYYY), month (MM), and day (DD) (if date)
    """
    creation_time: typing.Optional[str] = pydantic.Field(
        alias="creationTime", default=None
    )
    """
    Provides a timestamp (UTC). Designates the hour (hh), minute (mm), seconds (ss) and date (if timestamp) or year (YYYY), month (MM), and day (DD) (if date)
    """
    custom_url: typing.Optional[str] = pydantic.Field(alias="customUrl", default=None)
    """
    A reference to a web resource on the internet specifying its location on a computer network and a mechanism for retrieving.
    """
    merchant_order_description: typing.Optional[str] = pydantic.Field(
        alias="merchantOrderDescription", default=None
    )
    """
    Merchant provided textual information about the goods and/or services purchased. This text may include details about the prices, quantity and description of goods and/or services to be delivered for all transactions included in the sale.
    """
    mobile_device: typing.Optional[bool] = pydantic.Field(
        alias="mobileDevice", default=None
    )
    """
    Indicate if the device placing the order a mobile device.
    """
    preferred_language: typing.Optional[str] = pydantic.Field(
        alias="preferredLanguage", default=None
    )
    """
    Language preference indicated by consumer for pages displayed. Using language tags indicated in RFC5646.
    """
    redirected_payment: typing.Optional[RedirectedPayment] = pydantic.Field(
        alias="redirectedPayment", default=None
    )
    """
    Redirected Payment attributes
    """
