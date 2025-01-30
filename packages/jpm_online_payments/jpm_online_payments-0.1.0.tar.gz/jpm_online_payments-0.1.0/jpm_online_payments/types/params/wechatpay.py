import typing
import typing_extensions
import pydantic

from .redirected_payment import RedirectedPayment, _SerializerRedirectedPayment


class Wechatpay(typing_extensions.TypedDict):
    """
    Wechatpay payment method is linked to consumer bank accounts and/or payment network cards
    """

    completion_time: typing_extensions.NotRequired[str]
    """
    Provides a timestamp (UTC). Designates the hour (hh), minute (mm), seconds (ss) and date (if timestamp) or year (YYYY), month (MM), and day (DD) (if date)
    """

    creation_time: typing_extensions.NotRequired[str]
    """
    Provides a timestamp (UTC). Designates the hour (hh), minute (mm), seconds (ss) and date (if timestamp) or year (YYYY), month (MM), and day (DD) (if date)
    """

    merchant_order_description: typing_extensions.NotRequired[str]
    """
    Merchant provided textual information about the goods and/or services purchased. This text may include details about the prices, quantity and description of goods and/or services to be delivered for all transactions included in the sale.
    """

    payment_arrangement_expiration_timestamp: typing_extensions.NotRequired[str]
    """
    Designates the hour (hh), minute (mm), seconds (ss) and date (if timestamp) or year (YYYY), month (MM), and day (DD) (if date) when the relationship expires. If there is no defined expiration date, the field will be blank.
    """

    preferred_language: typing_extensions.NotRequired[str]
    """
    Language preference indicated by consumer for pages displayed. Using language tags indicated in RFC5646.
    """

    qr_code_url: typing_extensions.NotRequired[str]
    """
    Information on where consumer needs to be redirected for payment process completion. Ensure that the URL begins with either 'http' or 'https'
    """

    redirected_payment: typing_extensions.NotRequired[RedirectedPayment]
    """
    Redirected Payment attributes
    """


class _SerializerWechatpay(pydantic.BaseModel):
    """
    Serializer for Wechatpay handling case conversions
    and file omissions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
        populate_by_name=True,
    )

    completion_time: typing.Optional[str] = pydantic.Field(
        alias="completionTime", default=None
    )
    creation_time: typing.Optional[str] = pydantic.Field(
        alias="creationTime", default=None
    )
    merchant_order_description: typing.Optional[str] = pydantic.Field(
        alias="merchantOrderDescription", default=None
    )
    payment_arrangement_expiration_timestamp: typing.Optional[str] = pydantic.Field(
        alias="paymentArrangementExpirationTimestamp", default=None
    )
    preferred_language: typing.Optional[str] = pydantic.Field(
        alias="preferredLanguage", default=None
    )
    qr_code_url: typing.Optional[str] = pydantic.Field(alias="qrCodeUrl", default=None)
    redirected_payment: typing.Optional[_SerializerRedirectedPayment] = pydantic.Field(
        alias="redirectedPayment", default=None
    )
