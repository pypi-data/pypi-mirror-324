import typing
import typing_extensions
import pydantic

from .additional_data import AdditionalData, _SerializerAdditionalData
from .billing_verification import BillingVerification, _SerializerBillingVerification
from .network_response_account_updater import (
    NetworkResponseAccountUpdater,
    _SerializerNetworkResponseAccountUpdater,
)


class NetworkResponse(typing_extensions.TypedDict):
    """
    Response information from payment network
    """

    additional_data: typing_extensions.NotRequired[AdditionalData]
    """
    Additional information received from the payment network.
    """

    address_verification_result: typing_extensions.NotRequired[
        typing_extensions.Literal[
            "ADDRESS_MATCH",
            "ADDRESS_POSTALCODE_MATCH",
            "NAME_ADDRESS_MATCH",
            "NAME_MATCH",
            "NAME_POSTALCODE_MATCH",
            "NOT_AVAILABLE",
            "NOT_REQUESTED",
            "NOT_VERIFIED",
            "NO_MATCH",
            "POSTALCODE_MATCH",
            "SERVICE_NOT_AVAILABLE_RETRY",
            "SERVICE_NOT_SUPPORTED",
        ]
    ]
    """
    Indicates which aspects of address included in payment request match according to issuer.
    """

    address_verification_result_code: typing_extensions.NotRequired[str]
    """
    Indicates the address verification result code (e.g. Z = zip code match, A = address match).
    """

    bank_net_date: typing_extensions.NotRequired[str]
    """
    Designates the year (YYYY), month (MM), and day (DD) the transaction was authorized at MasterCard.
    """

    banknet_reference_number: typing_extensions.NotRequired[str]
    """
    Identifies the number assigned by MasterCard to each authorization message between a card acceptor and an issuer.
    """

    billing_verification: typing_extensions.NotRequired[BillingVerification]
    """
    Billing Verification results from payment network
    """

    card_verification_result: typing_extensions.NotRequired[
        typing_extensions.Literal[
            "MATCH", "NOT_PRESENT", "NOT_PROCESSED", "NOT_SUPPORTED", "NO_MATCH"
        ]
    ]
    """
    Indicates if the card verification values (CVV/CV2) match.
    """

    card_verification_result_code: typing_extensions.NotRequired[str]
    """
    Indicates whether card holder authentication values matched or not. (e.g., M = CVV2 matched, N = CVV2 did not match).
    """

    debit_trace_number: typing_extensions.NotRequired[str]
    """
    Identifies a reference number generated at transaction time.
    """

    email_verification_result: typing_extensions.NotRequired[
        typing_extensions.Literal[
            "MATCH",
            "NOT_VERIFIED",
            "NO_MATCH",
            "SERVICE_NOT_AVAILABLE_RETRY",
            "SERVICE_NOT_SUPPORTED",
        ]
    ]
    """
    Provides the textual detail information of the issuer's authorization response code to a merchant when verifying the cardholder's email address to help authenticate transactions and prevent fraud. This is Amex only field.
    """

    email_verification_result_code: typing_extensions.NotRequired[str]
    """
    Indicates whether the account holder's email address matched or not. This is Amex only field.
    """

    last4_card_number: typing_extensions.NotRequired[str]
    """
    Masked Card Number
    """

    network_account_updater: typing_extensions.NotRequired[
        NetworkResponseAccountUpdater
    ]
    """
    Account update information as returned by the network
    """

    network_response_code: typing_extensions.NotRequired[str]
    """
    Network provided error or reason code
    """

    network_transaction_id: typing_extensions.NotRequired[str]
    """
    A unique identifier for the transaction returned by the issuer. For Mastercard, this includes the    BanknetReferenceNumber.
    """

    payment_account_reference: typing_extensions.NotRequired[str]
    """
    A unique identifier associated with a specific cardholder primary account number (PAN) used to link a payment account represented by that PAN to affiliated payment tokens. This 29 character identification number can be used in place of sensitive consumer identification fields, and transmitted across the payments ecosystem to facilitate consumer identification.
    """

    phone_verification_result: typing_extensions.NotRequired[
        typing_extensions.Literal[
            "MATCH",
            "NOT_VERIFIED",
            "NO_MATCH",
            "SERVICE_NOT_AVAILABLE_RETRY",
            "SERVICE_NOT_SUPPORTED",
        ]
    ]
    """
    Indicates whether the account holder's phone number matched or not. This is an Amex only field.
    """

    phone_verification_result_code: typing_extensions.NotRequired[str]
    """
    Provides the textual detail information of the issuer's authorization response code to a merchant when verifying the cardholder's billing telephone number to help authenticate transactions and prevent fraud. This is Amex only field.
    """

    point_of_sale_data_code: typing_extensions.NotRequired[str]
    """
    Code to identify terminal capability, security data, and specific conditions present at the time a transaction occurred at the point of sale.
    """

    token_assurance_score: typing_extensions.NotRequired[str]
    """
    Indicates assurance level associated with the token
    """

    token_requestor_identifier: typing_extensions.NotRequired[str]
    """
    Identifier for the merchant given by the token requestor
    """

    token_status: typing_extensions.NotRequired[str]
    """
    Indicates the status of the token. For Visa - A= Active for payment, I = Inactive for payment, S= Temporarily suspended for payments, D = Permanently deactivated for payments.
    """


class _SerializerNetworkResponse(pydantic.BaseModel):
    """
    Serializer for NetworkResponse handling case conversions
    and file omissions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
        populate_by_name=True,
    )

    additional_data: typing.Optional[_SerializerAdditionalData] = pydantic.Field(
        alias="additionalData", default=None
    )
    address_verification_result: typing.Optional[
        typing_extensions.Literal[
            "ADDRESS_MATCH",
            "ADDRESS_POSTALCODE_MATCH",
            "NAME_ADDRESS_MATCH",
            "NAME_MATCH",
            "NAME_POSTALCODE_MATCH",
            "NOT_AVAILABLE",
            "NOT_REQUESTED",
            "NOT_VERIFIED",
            "NO_MATCH",
            "POSTALCODE_MATCH",
            "SERVICE_NOT_AVAILABLE_RETRY",
            "SERVICE_NOT_SUPPORTED",
        ]
    ] = pydantic.Field(alias="addressVerificationResult", default=None)
    address_verification_result_code: typing.Optional[str] = pydantic.Field(
        alias="addressVerificationResultCode", default=None
    )
    bank_net_date: typing.Optional[str] = pydantic.Field(
        alias="bankNetDate", default=None
    )
    banknet_reference_number: typing.Optional[str] = pydantic.Field(
        alias="banknetReferenceNumber", default=None
    )
    billing_verification: typing.Optional[_SerializerBillingVerification] = (
        pydantic.Field(alias="billingVerification", default=None)
    )
    card_verification_result: typing.Optional[
        typing_extensions.Literal[
            "MATCH", "NOT_PRESENT", "NOT_PROCESSED", "NOT_SUPPORTED", "NO_MATCH"
        ]
    ] = pydantic.Field(alias="cardVerificationResult", default=None)
    card_verification_result_code: typing.Optional[str] = pydantic.Field(
        alias="cardVerificationResultCode", default=None
    )
    debit_trace_number: typing.Optional[str] = pydantic.Field(
        alias="debitTraceNumber", default=None
    )
    email_verification_result: typing.Optional[
        typing_extensions.Literal[
            "MATCH",
            "NOT_VERIFIED",
            "NO_MATCH",
            "SERVICE_NOT_AVAILABLE_RETRY",
            "SERVICE_NOT_SUPPORTED",
        ]
    ] = pydantic.Field(alias="emailVerificationResult", default=None)
    email_verification_result_code: typing.Optional[str] = pydantic.Field(
        alias="emailVerificationResultCode", default=None
    )
    last4_card_number: typing.Optional[str] = pydantic.Field(
        alias="last4CardNumber", default=None
    )
    network_account_updater: typing.Optional[
        _SerializerNetworkResponseAccountUpdater
    ] = pydantic.Field(alias="networkAccountUpdater", default=None)
    network_response_code: typing.Optional[str] = pydantic.Field(
        alias="networkResponseCode", default=None
    )
    network_transaction_id: typing.Optional[str] = pydantic.Field(
        alias="networkTransactionId", default=None
    )
    payment_account_reference: typing.Optional[str] = pydantic.Field(
        alias="paymentAccountReference", default=None
    )
    phone_verification_result: typing.Optional[
        typing_extensions.Literal[
            "MATCH",
            "NOT_VERIFIED",
            "NO_MATCH",
            "SERVICE_NOT_AVAILABLE_RETRY",
            "SERVICE_NOT_SUPPORTED",
        ]
    ] = pydantic.Field(alias="phoneVerificationResult", default=None)
    phone_verification_result_code: typing.Optional[str] = pydantic.Field(
        alias="phoneVerificationResultCode", default=None
    )
    point_of_sale_data_code: typing.Optional[str] = pydantic.Field(
        alias="pointOfSaleDataCode", default=None
    )
    token_assurance_score: typing.Optional[str] = pydantic.Field(
        alias="tokenAssuranceScore", default=None
    )
    token_requestor_identifier: typing.Optional[str] = pydantic.Field(
        alias="tokenRequestorIdentifier", default=None
    )
    token_status: typing.Optional[str] = pydantic.Field(
        alias="tokenStatus", default=None
    )
