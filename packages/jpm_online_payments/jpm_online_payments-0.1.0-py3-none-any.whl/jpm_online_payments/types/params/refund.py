import typing
import typing_extensions
import pydantic

from .account_holder import AccountHolder, _SerializerAccountHolder
from .mandate import Mandate, _SerializerMandate
from .merchant import Merchant, _SerializerMerchant
from .merchant_defined import MerchantDefined, _SerializerMerchantDefined
from .payment_metadata import PaymentMetadata, _SerializerPaymentMetadata
from .refund_payment_method_type import (
    RefundPaymentMethodType,
    _SerializerRefundPaymentMethodType,
)
from .point_of_interaction import PointOfInteraction, _SerializerPointOfInteraction
from .restaurant_addenda import RestaurantAddenda, _SerializerRestaurantAddenda
from .retail_addenda import RetailAddenda, _SerializerRetailAddenda
from .sub_merchant_supplemental_data import (
    SubMerchantSupplementalData,
    _SerializerSubMerchantSupplementalData,
)


class Refund(typing_extensions.TypedDict):
    """
    Input information for refund API calls
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

    amount: typing_extensions.NotRequired[int]
    """
    Total monetary value of the payment including all taxes and fees.
    """

    capture_id: typing_extensions.NotRequired[str]
    """
    Identifies a unique occurrence of a payment settlement request when the authorization is complete and the transaction is ready for settlement. The transaction can no longer be edited but can be voided.
    """

    currency: typing_extensions.NotRequired[
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

    payment_metadata_list: typing_extensions.NotRequired[typing.List[PaymentMetadata]]
    """
    Payment Metadata List
    """

    payment_method_type: typing_extensions.NotRequired[RefundPaymentMethodType]
    """
    Object with one of the payment method type applicable for refund processing
    """

    payment_request_id: typing_extensions.NotRequired[str]
    """
    Identifies a unique occurrence of an payment processing request from merchant that is associated with a purchase of goods and/or services. A payment request consist of authorization, captures and refunds.
    """

    point_of_interaction: typing_extensions.NotRequired[PointOfInteraction]
    """
    In store payment Information
    """

    restaurant_addenda: typing_extensions.NotRequired[RestaurantAddenda]
    """
    Restaurant Addenda
    """

    retail_addenda: typing_extensions.NotRequired[RetailAddenda]
    """
    Industry-specific attributes.
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


class _SerializerRefund(pydantic.BaseModel):
    """
    Serializer for Refund handling case conversions
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
    amount: typing.Optional[int] = pydantic.Field(alias="amount", default=None)
    capture_id: typing.Optional[str] = pydantic.Field(alias="captureId", default=None)
    currency: typing.Optional[
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
    ] = pydantic.Field(alias="currency", default=None)
    initiator_type: typing.Optional[
        typing_extensions.Literal["CARDHOLDER", "MERCHANT"]
    ] = pydantic.Field(alias="initiatorType", default=None)
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
    payment_metadata_list: typing.Optional[typing.List[_SerializerPaymentMetadata]] = (
        pydantic.Field(alias="paymentMetadataList", default=None)
    )
    payment_method_type: typing.Optional[_SerializerRefundPaymentMethodType] = (
        pydantic.Field(alias="paymentMethodType", default=None)
    )
    payment_request_id: typing.Optional[str] = pydantic.Field(
        alias="paymentRequestId", default=None
    )
    point_of_interaction: typing.Optional[_SerializerPointOfInteraction] = (
        pydantic.Field(alias="pointOfInteraction", default=None)
    )
    restaurant_addenda: typing.Optional[_SerializerRestaurantAddenda] = pydantic.Field(
        alias="restaurantAddenda", default=None
    )
    retail_addenda: typing.Optional[_SerializerRetailAddenda] = pydantic.Field(
        alias="retailAddenda", default=None
    )
    statement_descriptor: typing.Optional[str] = pydantic.Field(
        alias="statementDescriptor", default=None
    )
    sub_merchant_supplemental_data: typing.Optional[
        _SerializerSubMerchantSupplementalData
    ] = pydantic.Field(alias="subMerchantSupplementalData", default=None)
