import typing
import typing_extensions
import pydantic

from .account_holder import AccountHolder, _SerializerAccountHolder
from .installment import Installment, _SerializerInstallment
from .merchant import Merchant, _SerializerMerchant
from .multi_capture import MultiCapture, _SerializerMultiCapture
from .multi_capture_payment_method_type import (
    MultiCapturePaymentMethodType,
    _SerializerMultiCapturePaymentMethodType,
)
from .recurring import Recurring, _SerializerRecurring
from .retail_addenda import RetailAddenda, _SerializerRetailAddenda
from .risk import Risk, _SerializerRisk
from .ship_to import ShipTo, _SerializerShipTo
from .sub_merchant_supplemental_data import (
    SubMerchantSupplementalData,
    _SerializerSubMerchantSupplementalData,
)


class CaptureRequest(typing_extensions.TypedDict):
    """
    Request information for capture a payment
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

    capture_method: typing_extensions.NotRequired[
        typing_extensions.Literal["DELAYED", "MANUAL", "NOW"]
    ]
    """
    To capture via separate API call, send captureMethod= ?Manual.? For immediate capture, send captureMethod= ?Now.? For automated delayed capture based on merchant profile setting (default is 120 minutes), send captureMethod= ?Delayed.?
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

    installment: typing_extensions.NotRequired[Installment]
    """
    Object containing information in the file
    """

    is_amount_final: typing_extensions.NotRequired[bool]
    """
    Indicates if the amount is final and will not change
    """

    merchant: typing_extensions.NotRequired[Merchant]
    """
    Information about the merchant
    """

    merchant_order_number: typing_extensions.NotRequired[str]
    """
    A unique merchant assigned identifier for the confirmation of goods and/or services purchased. The merchant order provides the merchant a reference to the prices, quantity and description of goods and/or services to be delivered for all transactions included in the sale.
    """

    multi_capture: typing_extensions.NotRequired[MultiCapture]
    """
    Split Shipment Information
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

    payment_method_type: typing_extensions.NotRequired[MultiCapturePaymentMethodType]
    """
    Multi Capture Payment Method Type contains all the payment method code supported for multi capture payment processing capability
    """

    payment_request_id: typing_extensions.NotRequired[str]
    """
    Identifies a unique occurrence of an payment processing request from merchant that is associated with a purchase of goods and/or services. A payment request consist of authorization, captures and refunds.
    """

    recurring: typing_extensions.NotRequired[Recurring]
    """
    Recurring Payment Object
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


class _SerializerCaptureRequest(pydantic.BaseModel):
    """
    Serializer for CaptureRequest handling case conversions
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
    capture_method: typing.Optional[
        typing_extensions.Literal["DELAYED", "MANUAL", "NOW"]
    ] = pydantic.Field(alias="captureMethod", default=None)
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
    installment: typing.Optional[_SerializerInstallment] = pydantic.Field(
        alias="installment", default=None
    )
    is_amount_final: typing.Optional[bool] = pydantic.Field(
        alias="isAmountFinal", default=None
    )
    merchant: typing.Optional[_SerializerMerchant] = pydantic.Field(
        alias="merchant", default=None
    )
    merchant_order_number: typing.Optional[str] = pydantic.Field(
        alias="merchantOrderNumber", default=None
    )
    multi_capture: typing.Optional[_SerializerMultiCapture] = pydantic.Field(
        alias="multiCapture", default=None
    )
    original_transaction_id: typing.Optional[str] = pydantic.Field(
        alias="originalTransactionId", default=None
    )
    partial_authorization_support: typing.Optional[
        typing_extensions.Literal["NOT_SUPPORTED", "SUPPORTED"]
    ] = pydantic.Field(alias="partialAuthorizationSupport", default=None)
    payment_method_type: typing.Optional[_SerializerMultiCapturePaymentMethodType] = (
        pydantic.Field(alias="paymentMethodType", default=None)
    )
    payment_request_id: typing.Optional[str] = pydantic.Field(
        alias="paymentRequestId", default=None
    )
    recurring: typing.Optional[_SerializerRecurring] = pydantic.Field(
        alias="recurring", default=None
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
