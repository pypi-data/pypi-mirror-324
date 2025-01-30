import typing
import typing_extensions
import pydantic

from .authentication import Authentication
from .payment_authentication_request import PaymentAuthenticationRequest


class VerificationConsumerProfile(pydantic.BaseModel):
    """
    Consumer Profile Payment method and attributes needed to process a verification transaction.
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    account_type: typing.Optional[
        typing_extensions.Literal["CHECKING", "CORPORATE_CHECKING", "SAVING"]
    ] = pydantic.Field(alias="accountType", default=None)
    """
    Type of banking account.
    """
    ach_verification_type: typing.Optional[
        typing_extensions.Literal[
            "ACCOUNT_OWNER",
            "ACCOUNT_STATUS",
            "BASIC",
            "PRE_NOTE_CREDIT",
            "PRE_NOTE_DEBIT",
        ]
    ] = pydantic.Field(alias="achVerificationType", default=None)
    """
    Indicates the type of ACH verification being performed.
    """
    authentication: typing.Optional[Authentication] = pydantic.Field(
        alias="authentication", default=None
    )
    """
    The authentication object allows you to opt in to additional security features like 3-D Secure
    """
    consumer_profile_id: str = pydantic.Field(
        alias="consumerProfileId",
    )
    """
    Identifies a unique occurrence of a consumer maintained in the firm as requested by merchant. Consumer profile contains information relevant to processing transactions such as name, address, account and payment methods information.
    """
    consumer_verification_id: typing.Optional[str] = pydantic.Field(
        alias="consumerVerificationId", default=None
    )
    """
    A unique identifier assigned by a government agency. Examples include Driver's License number, green card id, and Passport number.
    """
    consumer_verification_id_state: typing.Optional[str] = pydantic.Field(
        alias="consumerVerificationIdState", default=None
    )
    """
    Classifies a geographic area that represents a first level, legal and political subdivision of a country; for example, Virginia, Bavaria.
    """
    consumer_verification_id_type: typing.Optional[
        typing_extensions.Literal[
            "CAN_DL",
            "FOREIGN_DL",
            "MAT_CONSULAR_ID",
            "MEX_DL",
            "OTH_PRIM_ID",
            "PASSPORT",
            "RES_ALIEN_ID",
            "STATE_ID",
            "STUDENT_ID",
            "US_DL",
            "US_MILITARY",
        ]
    ] = pydantic.Field(alias="consumerVerificationIdType", default=None)
    """
    Classifies the type of identifier.
    """
    cvv: typing.Optional[str] = pydantic.Field(alias="cvv", default=None)
    """
    Card verification value (CVV/CV2)
    """
    individual_birth_date: typing.Optional[str] = pydantic.Field(
        alias="individualBirthDate", default=None
    )
    """
    Specifies the year month and day on which the individual was born.
    """
    is_bill_payment: typing.Optional[bool] = pydantic.Field(
        alias="isBillPayment", default=None
    )
    """
    Indicates whether or not the transaction is identified as a bill payment, prearranged between the cardholder and the merchant.
    """
    last4_ssn: typing.Optional[str] = pydantic.Field(alias="last4SSN", default=None)
    """
    Identifies the last four digits of the government issued (SSN, EIN, TIN).
    """
    merchant_sales_channel_name: typing.Optional[
        typing_extensions.Literal[
            "INTERACTIVE_VOICE_RESPONSE", "INTERNET", "MAIL_ORDER_TELEPHONE_ORDER"
        ]
    ] = pydantic.Field(alias="merchantSalesChannelName", default=None)
    """
    Label given to a merchant client of the Firm's medium for reaching its customers and facilitating and/or performing sales of its merchandise or services.
    """
    original_network_transaction_id: typing.Optional[str] = pydantic.Field(
        alias="originalNetworkTransactionId", default=None
    )
    """
    When submitting a merchant-initiated payment, submit the networkTransactionId received from the first payment in this field.
    """
    payment_method_id: typing.Optional[str] = pydantic.Field(
        alias="paymentMethodId", default=None
    )
    """
    Identifies a unique occurrence of the type of payment accepted by a level of the hierarchy of the merchant acquiring account.
    """
    payment_type: typing.Optional[
        typing_extensions.Literal["RECURRING", "TEL", "WEB"]
    ] = pydantic.Field(alias="paymentType", default=None)
    """
    Identifies how accountholders  initiated debits to their accounts .
    """
    verification_authentication_request: typing.Optional[
        PaymentAuthenticationRequest
    ] = pydantic.Field(alias="verificationAuthenticationRequest", default=None)
    """
    Request Authentication during payment process
    """
