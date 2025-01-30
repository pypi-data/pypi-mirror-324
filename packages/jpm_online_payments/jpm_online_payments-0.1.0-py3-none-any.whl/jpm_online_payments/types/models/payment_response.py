import typing
import typing_extensions
import pydantic

from .account_holder import AccountHolder
from .direct_pay import DirectPay
from .information import Information
from .installment import Installment
from .mandate import Mandate
from .merchant import Merchant
from .merchant_defined import MerchantDefined
from .multi_capture import MultiCapture
from .payment_authentication_result import PaymentAuthenticationResult
from .payment_method_type import PaymentMethodType
from .payment_request import PaymentRequest
from .point_of_interaction import PointOfInteraction
from .recurring import Recurring
from .restaurant_addenda import RestaurantAddenda
from .retail_addenda import RetailAddenda
from .risk import Risk
from .ship_to import ShipTo
from .source_account_information import SourceAccountInformation
from .sub_merchant_supplemental_data import SubMerchantSupplementalData


class PaymentResponse(pydantic.BaseModel):
    """
    Response information for payment API calls
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
    amount: typing.Optional[int] = pydantic.Field(alias="amount", default=None)
    """
    Total monetary value of the payment including all taxes and fees.
    """
    approval_code: typing.Optional[str] = pydantic.Field(
        alias="approvalCode", default=None
    )
    """
    Approval code provided by the issuing bank.
    """
    authorization_purpose: typing.Optional[
        typing_extensions.Literal[
            "DELAYED_CHARGE", "NO_SHOW", "REAUTHORIZATION", "RESUBMISSION"
        ]
    ] = pydantic.Field(alias="authorizationPurpose", default=None)
    """
    This field should be populated when there is a specific authorization purpose such as delayed authorizations, reauthorizations, resubmissions and no shows.
    """
    balance_authorization_amount: typing.Optional[int] = pydantic.Field(
        alias="balanceAuthorizationAmount", default=None
    )
    """
    The amount returned by the issuer which indicates the balance left on the card.
    """
    capture_method: typing.Optional[
        typing_extensions.Literal["DELAYED", "MANUAL", "NOW"]
    ] = pydantic.Field(alias="captureMethod", default=None)
    """
    To capture via separate API call, send captureMethod= ?Manual.? For immediate capture, send captureMethod= ?Now.? For automated delayed capture based on merchant profile setting (default is 120 minutes), send captureMethod= ?Delayed.?
    """
    capture_time: typing.Optional[str] = pydantic.Field(
        alias="captureTime", default=None
    )
    """
    Timestamp when delayed capture payment is scheduled to be automatically captured, at which point it can no longer be edited or voided.
    """
    cash_back_amount: typing.Optional[int] = pydantic.Field(
        alias="cashBackAmount", default=None
    )
    """
    The monetary value of a cash withdrawal using a debit or credit card during checkout at a physical terminal in a merchant location. Cash back is equivalent to withdrawing cash from an Automated Teller Machine (ATM).
    """
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
    """
    Describes the currency type of the transaction
    """
    direct_pay: typing.Optional[DirectPay] = pydantic.Field(
        alias="directPay", default=None
    )
    """
    Direct Pay
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
    external_order_reference_number: typing.Optional[str] = pydantic.Field(
        alias="externalOrderReferenceNumber", default=None
    )
    """
    The identifier that payment method returns after the order placed in their system.
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
    installment: typing.Optional[Installment] = pydantic.Field(
        alias="installment", default=None
    )
    """
    Object containing information in the file
    """
    is_amount_final: typing.Optional[bool] = pydantic.Field(
        alias="isAmountFinal", default=None
    )
    """
    Indicates if the amount is final and will not change
    """
    is_capture: typing.Optional[bool] = pydantic.Field(alias="isCapture", default=None)
    """
    (Deprecated) For auth only, send isCapture=false. For sale or update an authorized payment to capture, send isCapture=true.
    """
    is_void: typing.Optional[bool] = pydantic.Field(alias="isVoid", default=None)
    """
    Void a payment
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
    multi_capture: typing.Optional[MultiCapture] = pydantic.Field(
        alias="multiCapture", default=None
    )
    """
    Split Shipment Information
    """
    original_transaction_id: typing.Optional[str] = pydantic.Field(
        alias="originalTransactionId", default=None
    )
    """
    Identifies a unique occurrence of a transaction.
    """
    partial_authorization: typing.Optional[bool] = pydantic.Field(
        alias="partialAuthorization", default=None
    )
    """
    Indicates that the issuer has provided the merchant an authorization for a portion of the amount requested. This service provides an alternative to receiving a decline when the available card balance is not sufficient to approve a transaction in full.
    """
    partial_authorization_support: typing.Optional[
        typing_extensions.Literal["NOT_SUPPORTED", "SUPPORTED"]
    ] = pydantic.Field(alias="partialAuthorizationSupport", default=None)
    """
    Indicates ability to support a partial approval amount on payments including prompting consumer for another method of payment for the balance.
    """
    payment_authentication_result: typing.Optional[PaymentAuthenticationResult] = (
        pydantic.Field(alias="paymentAuthenticationResult", default=None)
    )
    """
    Cardholder Authentication Result from the Payment request.
    """
    payment_method_type: PaymentMethodType = pydantic.Field(
        alias="paymentMethodType",
    )
    """
    paymentType
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
    remaining_auth_amount: typing.Optional[int] = pydantic.Field(
        alias="remainingAuthAmount", default=None
    )
    """
    Monetary value of uncaptured, approved authorizations currently being held against the card for this transaction by a given Merchant.
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
    requested_authorization_amount: typing.Optional[int] = pydantic.Field(
        alias="requestedAuthorizationAmount", default=None
    )
    """
    The authorized amount requested for either full or partial authorization by merchant.
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
    risk: typing.Optional[Risk] = pydantic.Field(alias="risk", default=None)
    """
    Response information for transactions
    """
    ship_to: typing.Optional[ShipTo] = pydantic.Field(alias="shipTo", default=None)
    """
    Object containing information about the recipients
    """
    source_account_information: typing.Optional[SourceAccountInformation] = (
        pydantic.Field(alias="sourceAccountInformation", default=None)
    )
    """
    Source Account Information
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
    total_authorized_amount: typing.Optional[int] = pydantic.Field(
        alias="totalAuthorizedAmount", default=None
    )
    """
    Specifies the monetary value of authorizations currently being held against the Card. For zero exponent currency codes (i.e. Japanese Yen) a virtual decimal of 2 is not expected.
    """
    transaction_date: typing.Optional[str] = pydantic.Field(
        alias="transactionDate", default=None
    )
    """
    Designates the hour, minute, seconds and date (if timestamp) or year, month, and date (if date) when the transaction (monetary or non-monetary) occurred.
    """
    transaction_id: str = pydantic.Field(
        alias="transactionId",
    )
    """
    Identifier of a transaction.
    """
    transaction_processor: typing.Optional[str] = pydantic.Field(
        alias="transactionProcessor", default=None
    )
    """
    Codifies specific system a client's program operates on within the Firm and through which cardholder transactions are submitted and processed
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
