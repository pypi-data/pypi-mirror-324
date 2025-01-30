import typing
import pydantic

from .redirected_payment import RedirectedPayment


class Wechatpay(pydantic.BaseModel):
    """
    Wechatpay payment method is linked to consumer bank accounts and/or payment network cards
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
    merchant_order_description: typing.Optional[str] = pydantic.Field(
        alias="merchantOrderDescription", default=None
    )
    """
    Merchant provided textual information about the goods and/or services purchased. This text may include details about the prices, quantity and description of goods and/or services to be delivered for all transactions included in the sale.
    """
    payment_arrangement_expiration_timestamp: typing.Optional[str] = pydantic.Field(
        alias="paymentArrangementExpirationTimestamp", default=None
    )
    """
    Designates the hour (hh), minute (mm), seconds (ss) and date (if timestamp) or year (YYYY), month (MM), and day (DD) (if date) when the relationship expires. If there is no defined expiration date, the field will be blank.
    """
    preferred_language: typing.Optional[str] = pydantic.Field(
        alias="preferredLanguage", default=None
    )
    """
    Language preference indicated by consumer for pages displayed. Using language tags indicated in RFC5646.
    """
    qr_code_url: typing.Optional[str] = pydantic.Field(alias="qrCodeUrl", default=None)
    """
    Information on where consumer needs to be redirected for payment process completion. Ensure that the URL begins with either 'http' or 'https'
    """
    redirected_payment: typing.Optional[RedirectedPayment] = pydantic.Field(
        alias="redirectedPayment", default=None
    )
    """
    Redirected Payment attributes
    """
