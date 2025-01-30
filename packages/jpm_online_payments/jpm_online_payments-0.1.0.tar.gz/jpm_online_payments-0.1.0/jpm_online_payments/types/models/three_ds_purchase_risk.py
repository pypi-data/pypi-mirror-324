import typing
import typing_extensions
import pydantic


class ThreeDsPurchaseRisk(pydantic.BaseModel):
    """
    Contains Risk related information provided by the  3DS Requestor.
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    delivery_timeframe: typing.Optional[
        typing_extensions.Literal["ELECTRONIC", "OVERNIGHT", "SAME_DAY", "TWO_OR_MORE"]
    ] = pydantic.Field(alias="deliveryTimeframe", default=None)
    """
    Indicates the merchandise delivery timeframe
    """
    order_email_address: typing.Optional[str] = pydantic.Field(
        alias="orderEmailAddress", default=None
    )
    """
    For electronic delivery, the email address to which the merchandise was delivered
    """
    pre_order_date: typing.Optional[str] = pydantic.Field(
        alias="preOrderDate", default=None
    )
    """
    For a pre-ordered purchase, the expected date that the merchandise will be available
    """
    prepaid_card_currency: typing.Optional[
        typing_extensions.Literal[
            "AED",
            "AFN",
            "ALL",
            "AMD",
            "ANG",
            "AOA",
            "ARS",
            "AUD",
            "AWG",
            "AZN",
            "BAM",
            "BBD",
            "BDT",
            "BGN",
            "BIF",
            "BMD",
            "BND",
            "BOB",
            "BRL",
            "BSD",
            "BTN",
            "BWP",
            "BYN",
            "BZD",
            "CAD",
            "CDF",
            "CHF",
            "CLP",
            "CNY",
            "COP",
            "CRC",
            "CVE",
            "CZK",
            "DJF",
            "DKK",
            "DOP",
            "DZD",
            "EGP",
            "ETB",
            "EUR",
            "FJD",
            "FKP",
            "GBP",
            "GEL",
            "GHS",
            "GIP",
            "GMD",
            "GTQ",
            "GYD",
            "HKD",
            "HNL",
            "HRK",
            "HTG",
            "HUF",
            "IDR",
            "ILS",
            "INR",
            "ISK",
            "JMD",
            "JPY",
            "KES",
            "KHR",
            "KMF",
            "KRW",
            "KYD",
            "KZT",
            "LAK",
            "LBP",
            "LKR",
            "LRD",
            "LSL",
            "MAD",
            "MDL",
            "MGA",
            "MKD",
            "MMK",
            "MNT",
            "MOP",
            "MRU",
            "MUR",
            "MVR",
            "MWK",
            "MXN",
            "MYR",
            "MZN",
            "NAD",
            "NGN",
            "NIO",
            "NOK",
            "NPR",
            "NZD",
            "PAB",
            "PEN",
            "PGK",
            "PHP",
            "PKR",
            "PLN",
            "PYG",
            "QAR",
            "RON",
            "RSD",
            "RWF",
            "SAR",
            "SBD",
            "SCR",
            "SEK",
            "SGD",
            "SHP",
            "SLL",
            "SOS",
            "SRD",
            "STN",
            "SZL",
            "THB",
            "TJS",
            "TOP",
            "TRY",
            "TTD",
            "TWD",
            "TZS",
            "UAH",
            "UGX",
            "USD",
            "UYU",
            "UZS",
            "VND",
            "VUV",
            "WST",
            "XAF",
            "XCD",
            "XOF",
            "XPF",
            "YER",
            "ZAR",
            "ZMW",
        ]
    ] = pydantic.Field(alias="prepaidCardCurrency", default=None)
    """
    Describes the currency type of the transaction
    """
    product_availability_code: typing.Optional[
        typing_extensions.Literal["AVAILABLE", "FUTURE"]
    ] = pydantic.Field(alias="productAvailabilityCode", default=None)
    """
    Indicates whether Cardholder is placing an order for merchandise with a future availability or release date.
    """
    product_repurchase_indicator: typing.Optional[bool] = pydantic.Field(
        alias="productRepurchaseIndicator", default=None
    )
    """
    Indicates whether the cardholder is reordering previously purchased merchandise.
    """
    purchased_prepaid_card_count: typing.Optional[int] = pydantic.Field(
        alias="purchasedPrepaidCardCount", default=None
    )
    """
    For prepaid or gift card purchase, total count of individual prepaid or gift cards/codes purchased.
    """
    purchased_prepaid_card_total_amount: typing.Optional[int] = pydantic.Field(
        alias="purchasedPrepaidCardTotalAmount", default=None
    )
    """
    For prepaid or gift card purchase, the purchase amount total of prepaid or gift card(s)
    """
    shipment_type: typing.Optional[
        typing_extensions.Literal[
            "ADDRESS_ON_FILE",
            "CARDHOLDER_ADDRESS",
            "DIGITAL_GOODS",
            "NOT_ON_FILE",
            "OTHER",
            "SHIP_TO_STORE",
            "TICKETS",
        ]
    ] = pydantic.Field(alias="shipmentType", default=None)
    """
    Indicates shipping method chosen for the transaction.
    """
