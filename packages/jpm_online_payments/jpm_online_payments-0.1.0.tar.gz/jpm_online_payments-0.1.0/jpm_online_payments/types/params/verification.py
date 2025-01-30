import typing
import typing_extensions
import pydantic

from .account_holder import AccountHolder, _SerializerAccountHolder
from .browser_info import BrowserInfo, _SerializerBrowserInfo
from .installment import Installment, _SerializerInstallment
from .mandate import Mandate, _SerializerMandate
from .merchant import Merchant, _SerializerMerchant
from .payment_metadata import PaymentMetadata, _SerializerPaymentMetadata
from .verification_payment_method_type import (
    VerificationPaymentMethodType,
    _SerializerVerificationPaymentMethodType,
)
from .sub_merchant_supplemental_data import (
    SubMerchantSupplementalData,
    _SerializerSubMerchantSupplementalData,
)


class Verification(typing_extensions.TypedDict):
    """
    Input verification information for API call
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

    browser_info: typing_extensions.NotRequired[BrowserInfo]
    """
    Browser Information of the consumer
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

    mandate: typing_extensions.NotRequired[Mandate]
    """
    Agreement information between the consumer, debtor bank (checking account of the consumer) and the merchant for debit funds.
    """

    merchant: typing_extensions.Required[Merchant]
    """
    Information about the merchant
    """

    merchant_order_number: typing_extensions.NotRequired[str]
    """
    A unique merchant assigned identifier for the confirmation of goods and/or services purchased. The merchant order provides the merchant a reference to the prices, quantity and description of goods and/or services to be delivered for all transactions included in the sale.
    """

    payment_metadata_list: typing_extensions.NotRequired[typing.List[PaymentMetadata]]
    """
    Payment Metadata List
    """

    payment_method_type: typing_extensions.Required[VerificationPaymentMethodType]
    """
    Object with one of the payment method type applicable for verification processing
    """

    recurring_sequence: typing_extensions.NotRequired[
        typing_extensions.Literal["FIRST", "SUBSEQUENT"]
    ]
    """
    Identifies whether payment is the first in a series of recurring payments or a subsequent payment. Required for recurring billing.
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

    website_short_merchant_universal_resource_locator_text: (
        typing_extensions.NotRequired[str]
    )
    """
    Provides textual information about data for the protocol for specifying addresses on the Internet (Universal Resource Locator - URL) for the merchant's organization.
    """


class _SerializerVerification(pydantic.BaseModel):
    """
    Serializer for Verification handling case conversions
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
    browser_info: typing.Optional[_SerializerBrowserInfo] = pydantic.Field(
        alias="browserInfo", default=None
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
    initiator_type: typing.Optional[
        typing_extensions.Literal["CARDHOLDER", "MERCHANT"]
    ] = pydantic.Field(alias="initiatorType", default=None)
    installment: typing.Optional[_SerializerInstallment] = pydantic.Field(
        alias="installment", default=None
    )
    mandate: typing.Optional[_SerializerMandate] = pydantic.Field(
        alias="mandate", default=None
    )
    merchant: _SerializerMerchant = pydantic.Field(
        alias="merchant",
    )
    merchant_order_number: typing.Optional[str] = pydantic.Field(
        alias="merchantOrderNumber", default=None
    )
    payment_metadata_list: typing.Optional[typing.List[_SerializerPaymentMetadata]] = (
        pydantic.Field(alias="paymentMetadataList", default=None)
    )
    payment_method_type: _SerializerVerificationPaymentMethodType = pydantic.Field(
        alias="paymentMethodType",
    )
    recurring_sequence: typing.Optional[
        typing_extensions.Literal["FIRST", "SUBSEQUENT"]
    ] = pydantic.Field(alias="recurringSequence", default=None)
    sub_merchant_supplemental_data: typing.Optional[
        _SerializerSubMerchantSupplementalData
    ] = pydantic.Field(alias="subMerchantSupplementalData", default=None)
    transaction_routing_override_list: typing.Optional[
        typing.List[typing_extensions.Literal["CIELO", "GETNET", "REDECARD", "STONE"]]
    ] = pydantic.Field(alias="transactionRoutingOverrideList", default=None)
    website_short_merchant_universal_resource_locator_text: typing.Optional[str] = (
        pydantic.Field(
            alias="websiteShortMerchantUniversalResourceLocatorText", default=None
        )
    )
