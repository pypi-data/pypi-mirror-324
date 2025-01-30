import typing
import typing_extensions
import pydantic

from .account_holder import AccountHolder, _SerializerAccountHolder
from .browser_info import BrowserInfo, _SerializerBrowserInfo
from .direct_pay import DirectPay, _SerializerDirectPay
from .installment import Installment, _SerializerInstallment
from .mandate import Mandate, _SerializerMandate
from .merchant import Merchant, _SerializerMerchant
from .merchant_defined import MerchantDefined, _SerializerMerchantDefined
from .payment_metadata import PaymentMetadata, _SerializerPaymentMetadata
from .payment_method_type import PaymentMethodType, _SerializerPaymentMethodType
from .point_of_interaction import PointOfInteraction, _SerializerPointOfInteraction
from .recurring import Recurring, _SerializerRecurring
from .restaurant_addenda import RestaurantAddenda, _SerializerRestaurantAddenda
from .retail_addenda import RetailAddenda, _SerializerRetailAddenda
from .risk import Risk, _SerializerRisk
from .ship_to import ShipTo, _SerializerShipTo
from .sub_merchant_supplemental_data import (
    SubMerchantSupplementalData,
    _SerializerSubMerchantSupplementalData,
)


class Payment(typing_extensions.TypedDict):
    """
    Request information for payment endpoint
    """

    account_holder: typing_extensions.NotRequired[AccountHolder]
    """
    Card owner properties
    """

    account_on_file: typing_extensions.NotRequired[
        typing_extensions.Literal["NOT_STORED", "STORED", "TO_BE_STORED"]
    ]
    """
    Indicates whether payment method is stored by merchant. Possible values:STORED - Use if already stored and current payment is either cardholder-initiated stored payment or subsequent recurring or installment transaction. NOT_STORED - Use when payment method obtained for purpose of single payment. TO_BE_STORED - Use when consumer is intentionally storing their payment method after this payment for subsequent recurring or stored payments.
    """

    amount: typing_extensions.Required[int]
    """
    Total monetary value of the payment including all taxes and fees.
    """

    authorization_purpose: typing_extensions.NotRequired[
        typing_extensions.Literal[
            "DELAYED_CHARGE", "NO_SHOW", "REAUTHORIZATION", "RESUBMISSION"
        ]
    ]
    """
    This field should be populated when there is a specific authorization purpose such as delayed authorizations, reauthorizations, resubmissions and no shows.
    """

    browser_info: typing_extensions.NotRequired[BrowserInfo]
    """
    Browser Information of the consumer
    """

    capture_method: typing_extensions.NotRequired[
        typing_extensions.Literal["DELAYED", "MANUAL", "NOW"]
    ]
    """
    To capture via separate API call, send captureMethod= ?Manual.? For immediate capture, send captureMethod= ?Now.? For automated delayed capture based on merchant profile setting (default is 120 minutes), send captureMethod= ?Delayed.?
    """

    cash_back_amount: typing_extensions.NotRequired[int]
    """
    The monetary value of a cash withdrawal using a debit or credit card during checkout at a physical terminal in a merchant location. Cash back is equivalent to withdrawing cash from an Automated Teller Machine (ATM).
    """

    currency: typing_extensions.Required[
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

    direct_pay: typing_extensions.NotRequired[DirectPay]
    """
    Direct Pay
    """

    initiator_type: typing_extensions.NotRequired[
        typing_extensions.Literal["CARDHOLDER", "MERCHANT"]
    ]
    """
    Describes the initiator of the transaction for the stored credential framework (MIT/CIT)
    """

    installment: typing_extensions.NotRequired[Installment]
    """
    Object containing information in the file
    """

    is_amount_final: typing_extensions.NotRequired[bool]
    """
    Indicates if the amount is final and will not change
    """

    is_capture: typing_extensions.NotRequired[bool]
    """
    (Deprecated) For auth only, send isCapture=false. For sale or update an authorized payment to capture, send isCapture=true.
    """

    mandate: typing_extensions.NotRequired[Mandate]
    """
    Agreement information between the consumer, debtor bank (checking account of the consumer) and the merchant for debit funds.
    """

    merchant: typing_extensions.Required[Merchant]
    """
    Information about the merchant
    """

    merchant_defined: typing_extensions.NotRequired[MerchantDefined]
    """
    merchant defined data field that it will pass through to reporting.
    """

    merchant_order_number: typing_extensions.NotRequired[str]
    """
    A unique merchant assigned identifier for the confirmation of goods and/or services purchased. The merchant order provides the merchant a reference to the prices, quantity and description of goods and/or services to be delivered for all transactions included in the sale.
    """

    original_transaction_id: typing_extensions.NotRequired[str]
    """
    Identifies a unique occurrence of a transaction.
    """

    partial_authorization_support: typing_extensions.NotRequired[
        typing_extensions.Literal["NOT_SUPPORTED", "SUPPORTED"]
    ]
    """
    Indicates ability to support a partial approval amount on payments including prompting consumer for another method of payment for the balance.
    """

    payment_metadata_list: typing_extensions.NotRequired[typing.List[PaymentMetadata]]
    """
    Payment Metadata List
    """

    payment_method_type: typing_extensions.Required[PaymentMethodType]
    """
    paymentType
    """

    point_of_interaction: typing_extensions.NotRequired[PointOfInteraction]
    """
    In store payment Information
    """

    recurring: typing_extensions.NotRequired[Recurring]
    """
    Recurring Payment Object
    """

    restaurant_addenda: typing_extensions.NotRequired[RestaurantAddenda]
    """
    Restaurant Addenda
    """

    retail_addenda: typing_extensions.NotRequired[RetailAddenda]
    """
    Industry-specific attributes.
    """

    risk: typing_extensions.NotRequired[Risk]
    """
    Response information for transactions
    """

    ship_to: typing_extensions.NotRequired[ShipTo]
    """
    Object containing information about the recipients
    """

    statement_descriptor: typing_extensions.NotRequired[str]
    """
    Merchant name to appear on account holder statement. If not provided, defaults to merchant profile descriptor value.  To send both company identifier and transaction-specific information, use one of these formats: Option 1 ? 3-byte company identifier * 18-byte descriptor (example: XYZ*PAYMENT1OF3) Option 2 ? 7-byte company identifier * 14-byte descriptor (example: XYZCOMP*PAYMENT1OF3) Option 3 ? 12-byte company identifier * 9-byte descriptor (example: XYZCOMPANY1*PAYMT1OF3)
    """

    sub_merchant_supplemental_data: typing_extensions.NotRequired[
        SubMerchantSupplementalData
    ]
    """
    Additional data provided by merchant for reference purposes.
    """

    transaction_routing_override_list: typing_extensions.NotRequired[
        typing.List[typing_extensions.Literal["CIELO", "GETNET", "REDECARD", "STONE"]]
    ]
    """
    List of transaction routing providers where the transaction be routed preferred by the merchant .
    """


class _SerializerPayment(pydantic.BaseModel):
    """
    Serializer for Payment handling case conversions
    and file omissions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
        populate_by_name=True,
    )

    account_holder: typing.Optional[_SerializerAccountHolder] = pydantic.Field(
        alias="accountHolder", default=None
    )
    account_on_file: typing.Optional[
        typing_extensions.Literal["NOT_STORED", "STORED", "TO_BE_STORED"]
    ] = pydantic.Field(alias="accountOnFile", default=None)
    amount: int = pydantic.Field(
        alias="amount",
    )
    authorization_purpose: typing.Optional[
        typing_extensions.Literal[
            "DELAYED_CHARGE", "NO_SHOW", "REAUTHORIZATION", "RESUBMISSION"
        ]
    ] = pydantic.Field(alias="authorizationPurpose", default=None)
    browser_info: typing.Optional[_SerializerBrowserInfo] = pydantic.Field(
        alias="browserInfo", default=None
    )
    capture_method: typing.Optional[
        typing_extensions.Literal["DELAYED", "MANUAL", "NOW"]
    ] = pydantic.Field(alias="captureMethod", default=None)
    cash_back_amount: typing.Optional[int] = pydantic.Field(
        alias="cashBackAmount", default=None
    )
    currency: typing_extensions.Literal[
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
    ] = pydantic.Field(
        alias="currency",
    )
    direct_pay: typing.Optional[_SerializerDirectPay] = pydantic.Field(
        alias="directPay", default=None
    )
    initiator_type: typing.Optional[
        typing_extensions.Literal["CARDHOLDER", "MERCHANT"]
    ] = pydantic.Field(alias="initiatorType", default=None)
    installment: typing.Optional[_SerializerInstallment] = pydantic.Field(
        alias="installment", default=None
    )
    is_amount_final: typing.Optional[bool] = pydantic.Field(
        alias="isAmountFinal", default=None
    )
    is_capture: typing.Optional[bool] = pydantic.Field(alias="isCapture", default=None)
    mandate: typing.Optional[_SerializerMandate] = pydantic.Field(
        alias="mandate", default=None
    )
    merchant: _SerializerMerchant = pydantic.Field(
        alias="merchant",
    )
    merchant_defined: typing.Optional[_SerializerMerchantDefined] = pydantic.Field(
        alias="merchantDefined", default=None
    )
    merchant_order_number: typing.Optional[str] = pydantic.Field(
        alias="merchantOrderNumber", default=None
    )
    original_transaction_id: typing.Optional[str] = pydantic.Field(
        alias="originalTransactionId", default=None
    )
    partial_authorization_support: typing.Optional[
        typing_extensions.Literal["NOT_SUPPORTED", "SUPPORTED"]
    ] = pydantic.Field(alias="partialAuthorizationSupport", default=None)
    payment_metadata_list: typing.Optional[typing.List[_SerializerPaymentMetadata]] = (
        pydantic.Field(alias="paymentMetadataList", default=None)
    )
    payment_method_type: _SerializerPaymentMethodType = pydantic.Field(
        alias="paymentMethodType",
    )
    point_of_interaction: typing.Optional[_SerializerPointOfInteraction] = (
        pydantic.Field(alias="pointOfInteraction", default=None)
    )
    recurring: typing.Optional[_SerializerRecurring] = pydantic.Field(
        alias="recurring", default=None
    )
    restaurant_addenda: typing.Optional[_SerializerRestaurantAddenda] = pydantic.Field(
        alias="restaurantAddenda", default=None
    )
    retail_addenda: typing.Optional[_SerializerRetailAddenda] = pydantic.Field(
        alias="retailAddenda", default=None
    )
    risk: typing.Optional[_SerializerRisk] = pydantic.Field(alias="risk", default=None)
    ship_to: typing.Optional[_SerializerShipTo] = pydantic.Field(
        alias="shipTo", default=None
    )
    statement_descriptor: typing.Optional[str] = pydantic.Field(
        alias="statementDescriptor", default=None
    )
    sub_merchant_supplemental_data: typing.Optional[
        _SerializerSubMerchantSupplementalData
    ] = pydantic.Field(alias="subMerchantSupplementalData", default=None)
    transaction_routing_override_list: typing.Optional[
        typing.List[typing_extensions.Literal["CIELO", "GETNET", "REDECARD", "STONE"]]
    ] = pydantic.Field(alias="transactionRoutingOverrideList", default=None)
