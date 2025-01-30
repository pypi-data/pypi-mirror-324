import typing
import typing_extensions
import pydantic

from .account_holder import AccountHolder
from .information import Information
from .mandate import Mandate
from .merchant import Merchant
from .merchant_defined import MerchantDefined
from .refund_payment_method_type import RefundPaymentMethodType
from .payment_request import PaymentRequest
from .point_of_interaction import PointOfInteraction
from .recurring import Recurring
from .restaurant_addenda import RestaurantAddenda
from .retail_addenda import RetailAddenda
from .sub_merchant_supplemental_data import SubMerchantSupplementalData


class RefundResponse(pydantic.BaseModel):
    """
    Response information for refund API calls
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    account_holder: typing.Optional[AccountHolder] = pydantic.Field(
        alias="accountHolder", default=None
    )
    """
    Card owner properties
    """
    account_on_file: typing.Optional[
        typing_extensions.Literal["NOT_STORED", "STORED", "TO_BE_STORED"]
    ] = pydantic.Field(alias="accountOnFile", default=None)
    """
    Indicates whether payment method is stored by merchant. Possible values:STORED - Use if already stored and current payment is either cardholder-initiated stored payment or subsequent recurring or installment transaction. NOT_STORED - Use when payment method obtained for purpose of single payment. TO_BE_STORED - Use when consumer is intentionally storing their payment method after this payment for subsequent recurring or stored payments.
    """
    amount: int = pydantic.Field(
        alias="amount",
    )
    """
    Total monetary value of the payment including all taxes and fees.
    """
    approval_code: typing.Optional[str] = pydantic.Field(
        alias="approvalCode", default=None
    )
    """
    Approval code provided by the issuing bank.
    """
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
    """
    Describes the currency type of the transaction
    """
    extended_host_error_code: typing.Optional[str] = pydantic.Field(
        alias="extendedHostErrorCode", default=None
    )
    """
    Codifies a raised exception encountered by an internal or external system, sub-system, interface, job, module, system component with which the web service application interfaces.In this instance it refers to the error returned from host system.
    """
    extended_host_message: typing.Optional[str] = pydantic.Field(
        alias="extendedHostMessage", default=None
    )
    """
    Message received from Issuer, network or processor. Can be blank
    """
    host_message: typing.Optional[str] = pydantic.Field(
        alias="hostMessage", default=None
    )
    """
    Message received from Issuer, network or processor. Can be blank
    """
    host_reference_id: typing.Optional[str] = pydantic.Field(
        alias="hostReferenceId", default=None
    )
    """
    Identifies unique identifier generated by the acquirer processing system and return to merchant for reference purposes.
    """
    information: typing.Optional[Information] = pydantic.Field(
        alias="information", default=None
    )
    """
    A list of informational messages
    """
    initiator_type: typing.Optional[
        typing_extensions.Literal["CARDHOLDER", "MERCHANT"]
    ] = pydantic.Field(alias="initiatorType", default=None)
    """
    Describes the initiator of the transaction for the stored credential framework (MIT/CIT)
    """
    mandate: typing.Optional[Mandate] = pydantic.Field(alias="mandate", default=None)
    """
    Agreement information between the consumer, debtor bank (checking account of the consumer) and the merchant for debit funds.
    """
    merchant: typing.Optional[Merchant] = pydantic.Field(alias="merchant", default=None)
    """
    Information about the merchant
    """
    merchant_defined: typing.Optional[MerchantDefined] = pydantic.Field(
        alias="merchantDefined", default=None
    )
    """
    merchant defined data field that it will pass through to reporting.
    """
    merchant_order_number: typing.Optional[str] = pydantic.Field(
        alias="merchantOrderNumber", default=None
    )
    """
    A unique merchant assigned identifier for the confirmation of goods and/or services purchased. The merchant order provides the merchant a reference to the prices, quantity and description of goods and/or services to be delivered for all transactions included in the sale.
    """
    payment_method_type: typing.Optional[RefundPaymentMethodType] = pydantic.Field(
        alias="paymentMethodType", default=None
    )
    """
    Object with one of the payment method type applicable for refund processing
    """
    payment_request: typing.Optional[PaymentRequest] = pydantic.Field(
        alias="paymentRequest", default=None
    )
    """
    Payment request information for multi capture order
    """
    point_of_interaction: typing.Optional[PointOfInteraction] = pydantic.Field(
        alias="pointOfInteraction", default=None
    )
    """
    In store payment Information
    """
    recurring: typing.Optional[Recurring] = pydantic.Field(
        alias="recurring", default=None
    )
    """
    Recurring Payment Object
    """
    remaining_refundable_amount: typing.Optional[int] = pydantic.Field(
        alias="remainingRefundableAmount", default=None
    )
    """
    This is the amount of the transaction that is currently available for refunds.  It takes into account the original transaction amount as well as any previous refunds that were applied to the transaction.
    """
    request_id: str = pydantic.Field(
        alias="requestId",
    )
    """
    Merchant identifier for the request. The value must be unique.
    """
    response_code: str = pydantic.Field(
        alias="responseCode",
    )
    """
    Short explanation for response status
    """
    response_message: str = pydantic.Field(
        alias="responseMessage",
    )
    """
    Long explanation of response code
    """
    response_status: typing_extensions.Literal["DENIED", "ERROR", "SUCCESS"] = (
        pydantic.Field(
            alias="responseStatus",
        )
    )
    """
    Indicates whether API request resulted in success, error, or denial.
    """
    restaurant_addenda: typing.Optional[RestaurantAddenda] = pydantic.Field(
        alias="restaurantAddenda", default=None
    )
    """
    Restaurant Addenda
    """
    retail_addenda: typing.Optional[RetailAddenda] = pydantic.Field(
        alias="retailAddenda", default=None
    )
    """
    Industry-specific attributes.
    """
    statement_descriptor: typing.Optional[str] = pydantic.Field(
        alias="statementDescriptor", default=None
    )
    """
    Merchant name to appear on account holder statement. If not provided, defaults to merchant profile descriptor value.  To send both company identifier and transaction-specific information, use one of these formats: Option 1 ? 3-byte company identifier * 18-byte descriptor (example: XYZ*PAYMENT1OF3) Option 2 ? 7-byte company identifier * 14-byte descriptor (example: XYZCOMP*PAYMENT1OF3) Option 3 ? 12-byte company identifier * 9-byte descriptor (example: XYZCOMPANY1*PAYMT1OF3)
    """
    sub_merchant_supplemental_data: typing.Optional[SubMerchantSupplementalData] = (
        pydantic.Field(alias="subMerchantSupplementalData", default=None)
    )
    """
    Additional data provided by merchant for reference purposes.
    """
    transaction_date: typing.Optional[str] = pydantic.Field(
        alias="transactionDate", default=None
    )
    """
    Designates the hour, minute, seconds and date (if timestamp) or year, month, and date (if date) when the transaction (monetary or non-monetary) occurred.
    """
    transaction_id: typing.Optional[str] = pydantic.Field(
        alias="transactionId", default=None
    )
    """
    Identifier of a transaction.
    """
    transaction_reference_id: typing.Optional[str] = pydantic.Field(
        alias="transactionReferenceId", default=None
    )
    """
    Reference to an existing payment.
    """
    transaction_routing_override_list: typing.Optional[
        typing.List[typing_extensions.Literal["CIELO", "GETNET", "REDECARD", "STONE"]]
    ] = pydantic.Field(alias="transactionRoutingOverrideList", default=None)
    """
    List of transaction routing providers where the transaction be routed preferred by the merchant .
    """
    transaction_state: typing_extensions.Literal[
        "AUTHORIZED", "CLOSED", "DECLINED", "ERROR", "PENDING", "VOIDED"
    ] = pydantic.Field(
        alias="transactionState",
    )
    """
    Current state transaction is in. "Authorized" - transaction not yet captured. "Captured" - can no longer be augmented. "Closed" - payout process initiated.
    """
