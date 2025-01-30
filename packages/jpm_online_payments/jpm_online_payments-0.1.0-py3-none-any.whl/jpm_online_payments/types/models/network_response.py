import typing
import typing_extensions
import pydantic

from .additional_data import AdditionalData
from .billing_verification import BillingVerification
from .network_response_account_updater import NetworkResponseAccountUpdater


class NetworkResponse(pydantic.BaseModel):
    """
    Response information from payment network
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    additional_data: typing.Optional[AdditionalData] = pydantic.Field(
        alias="additionalData", default=None
    )
    """
    Additional information received from the payment network.
    """
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
    """
    Indicates which aspects of address included in payment request match according to issuer.
    """
    address_verification_result_code: typing.Optional[str] = pydantic.Field(
        alias="addressVerificationResultCode", default=None
    )
    """
    Indicates the address verification result code (e.g. Z = zip code match, A = address match).
    """
    bank_net_date: typing.Optional[str] = pydantic.Field(
        alias="bankNetDate", default=None
    )
    """
    Designates the year (YYYY), month (MM), and day (DD) the transaction was authorized at MasterCard.
    """
    banknet_reference_number: typing.Optional[str] = pydantic.Field(
        alias="banknetReferenceNumber", default=None
    )
    """
    Identifies the number assigned by MasterCard to each authorization message between a card acceptor and an issuer.
    """
    billing_verification: typing.Optional[BillingVerification] = pydantic.Field(
        alias="billingVerification", default=None
    )
    """
    Billing Verification results from payment network
    """
    card_verification_result: typing.Optional[
        typing_extensions.Literal[
            "MATCH", "NOT_PRESENT", "NOT_PROCESSED", "NOT_SUPPORTED", "NO_MATCH"
        ]
    ] = pydantic.Field(alias="cardVerificationResult", default=None)
    """
    Indicates if the card verification values (CVV/CV2) match.
    """
    card_verification_result_code: typing.Optional[str] = pydantic.Field(
        alias="cardVerificationResultCode", default=None
    )
    """
    Indicates whether card holder authentication values matched or not. (e.g., M = CVV2 matched, N = CVV2 did not match).
    """
    debit_trace_number: typing.Optional[str] = pydantic.Field(
        alias="debitTraceNumber", default=None
    )
    """
    Identifies a reference number generated at transaction time.
    """
    email_verification_result: typing.Optional[
        typing_extensions.Literal[
            "MATCH",
            "NOT_VERIFIED",
            "NO_MATCH",
            "SERVICE_NOT_AVAILABLE_RETRY",
            "SERVICE_NOT_SUPPORTED",
        ]
    ] = pydantic.Field(alias="emailVerificationResult", default=None)
    """
    Provides the textual detail information of the issuer's authorization response code to a merchant when verifying the cardholder's email address to help authenticate transactions and prevent fraud. This is Amex only field.
    """
    email_verification_result_code: typing.Optional[str] = pydantic.Field(
        alias="emailVerificationResultCode", default=None
    )
    """
    Indicates whether the account holder's email address matched or not. This is Amex only field.
    """
    last4_card_number: typing.Optional[str] = pydantic.Field(
        alias="last4CardNumber", default=None
    )
    """
    Masked Card Number
    """
    network_account_updater: typing.Optional[NetworkResponseAccountUpdater] = (
        pydantic.Field(alias="networkAccountUpdater", default=None)
    )
    """
    Account update information as returned by the network
    """
    network_response_code: typing.Optional[str] = pydantic.Field(
        alias="networkResponseCode", default=None
    )
    """
    Network provided error or reason code
    """
    network_transaction_id: typing.Optional[str] = pydantic.Field(
        alias="networkTransactionId", default=None
    )
    """
    A unique identifier for the transaction returned by the issuer. For Mastercard, this includes the    BanknetReferenceNumber.
    """
    payment_account_reference: typing.Optional[str] = pydantic.Field(
        alias="paymentAccountReference", default=None
    )
    """
    A unique identifier associated with a specific cardholder primary account number (PAN) used to link a payment account represented by that PAN to affiliated payment tokens. This 29 character identification number can be used in place of sensitive consumer identification fields, and transmitted across the payments ecosystem to facilitate consumer identification.
    """
    phone_verification_result: typing.Optional[
        typing_extensions.Literal[
            "MATCH",
            "NOT_VERIFIED",
            "NO_MATCH",
            "SERVICE_NOT_AVAILABLE_RETRY",
            "SERVICE_NOT_SUPPORTED",
        ]
    ] = pydantic.Field(alias="phoneVerificationResult", default=None)
    """
    Indicates whether the account holder's phone number matched or not. This is an Amex only field.
    """
    phone_verification_result_code: typing.Optional[str] = pydantic.Field(
        alias="phoneVerificationResultCode", default=None
    )
    """
    Provides the textual detail information of the issuer's authorization response code to a merchant when verifying the cardholder's billing telephone number to help authenticate transactions and prevent fraud. This is Amex only field.
    """
    point_of_sale_data_code: typing.Optional[str] = pydantic.Field(
        alias="pointOfSaleDataCode", default=None
    )
    """
    Code to identify terminal capability, security data, and specific conditions present at the time a transaction occurred at the point of sale.
    """
    token_assurance_score: typing.Optional[str] = pydantic.Field(
        alias="tokenAssuranceScore", default=None
    )
    """
    Indicates assurance level associated with the token
    """
    token_requestor_identifier: typing.Optional[str] = pydantic.Field(
        alias="tokenRequestorIdentifier", default=None
    )
    """
    Identifier for the merchant given by the token requestor
    """
    token_status: typing.Optional[str] = pydantic.Field(
        alias="tokenStatus", default=None
    )
    """
    Indicates the status of the token. For Visa - A= Active for payment, I = Inactive for payment, S= Temporarily suspended for payments, D = Permanently deactivated for payments.
    """
