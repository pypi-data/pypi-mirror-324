import typing
import typing_extensions
import pydantic


class ThreeDsPurchaseRisk(typing_extensions.TypedDict):
    """
    Contains Risk related information provided by the  3DS Requestor.
    """

    delivery_timeframe: typing_extensions.NotRequired[
        typing_extensions.Literal["ELECTRONIC", "OVERNIGHT", "SAME_DAY", "TWO_OR_MORE"]
    ]
    """
    Indicates the merchandise delivery timeframe
    """

    order_email_address: typing_extensions.NotRequired[str]
    """
    For electronic delivery, the email address to which the merchandise was delivered
    """

    pre_order_date: typing_extensions.NotRequired[str]
    """
    For a pre-ordered purchase, the expected date that the merchandise will be available
    """

    prepaid_card_currency: typing_extensions.NotRequired[
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
    ]
    """
    Describes the currency type of the transaction
    """

    product_availability_code: typing_extensions.NotRequired[
        typing_extensions.Literal["AVAILABLE", "FUTURE"]
    ]
    """
    Indicates whether Cardholder is placing an order for merchandise with a future availability or release date.
    """

    product_repurchase_indicator: typing_extensions.NotRequired[bool]
    """
    Indicates whether the cardholder is reordering previously purchased merchandise.
    """

    purchased_prepaid_card_count: typing_extensions.NotRequired[int]
    """
    For prepaid or gift card purchase, total count of individual prepaid or gift cards/codes purchased.
    """

    purchased_prepaid_card_total_amount: typing_extensions.NotRequired[int]
    """
    For prepaid or gift card purchase, the purchase amount total of prepaid or gift card(s)
    """

    shipment_type: typing_extensions.NotRequired[
        typing_extensions.Literal[
            "ADDRESS_ON_FILE",
            "CARDHOLDER_ADDRESS",
            "DIGITAL_GOODS",
            "NOT_ON_FILE",
            "OTHER",
            "SHIP_TO_STORE",
            "TICKETS",
        ]
    ]
    """
    Indicates shipping method chosen for the transaction.
    """


class _SerializerThreeDsPurchaseRisk(pydantic.BaseModel):
    """
    Serializer for ThreeDsPurchaseRisk handling case conversions
    and file omissions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
        populate_by_name=True,
    )

    delivery_timeframe: typing.Optional[
        typing_extensions.Literal["ELECTRONIC", "OVERNIGHT", "SAME_DAY", "TWO_OR_MORE"]
    ] = pydantic.Field(alias="deliveryTimeframe", default=None)
    order_email_address: typing.Optional[str] = pydantic.Field(
        alias="orderEmailAddress", default=None
    )
    pre_order_date: typing.Optional[str] = pydantic.Field(
        alias="preOrderDate", default=None
    )
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
    product_availability_code: typing.Optional[
        typing_extensions.Literal["AVAILABLE", "FUTURE"]
    ] = pydantic.Field(alias="productAvailabilityCode", default=None)
    product_repurchase_indicator: typing.Optional[bool] = pydantic.Field(
        alias="productRepurchaseIndicator", default=None
    )
    purchased_prepaid_card_count: typing.Optional[int] = pydantic.Field(
        alias="purchasedPrepaidCardCount", default=None
    )
    purchased_prepaid_card_total_amount: typing.Optional[int] = pydantic.Field(
        alias="purchasedPrepaidCardTotalAmount", default=None
    )
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
