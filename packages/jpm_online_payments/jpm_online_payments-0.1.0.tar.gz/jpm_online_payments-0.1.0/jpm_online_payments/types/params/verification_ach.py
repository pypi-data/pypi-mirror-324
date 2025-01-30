import typing
import typing_extensions
import pydantic

from .payment_token import PaymentToken, _SerializerPaymentToken


class VerificationAch(typing_extensions.TypedDict):
    """
    Verification of ACH account
    """

    account_number: typing_extensions.NotRequired[str]
    """
    The card or token number.
    """

    account_type: typing_extensions.NotRequired[
        typing_extensions.Literal["CHECKING", "CORPORATE_CHECKING", "SAVING"]
    ]
    """
    Type of banking account.
    """

    ach_verification_type: typing_extensions.NotRequired[
        typing_extensions.Literal[
            "ACCOUNT_OWNER",
            "ACCOUNT_STATUS",
            "BASIC",
            "PRE_NOTE_CREDIT",
            "PRE_NOTE_DEBIT",
        ]
    ]
    """
    Indicates the type of ACH verification being performed.
    """

    consumer_verification_id: typing_extensions.NotRequired[str]
    """
    A unique identifier assigned by a government agency. Examples include Driver's License number, green card id, and Passport number.
    """

    consumer_verification_id_state: typing_extensions.NotRequired[str]
    """
    Classifies a geographic area that represents a first level, legal and political subdivision of a country; for example, Virginia, Bavaria.
    """

    consumer_verification_id_type: typing_extensions.NotRequired[
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
    ]
    """
    Classifies the type of identifier.
    """

    ecp_program_name: typing_extensions.NotRequired[str]
    """
    Label of the program used for backend processing when handling electronic or paper checks at point of sale, online or in-person.
    """

    financial_institution_routing_number: typing_extensions.NotRequired[str]
    """
    Identifies the routing and transit number. In the United  States it's 8-9 numeric characters.
    """

    individual_birth_date: typing_extensions.NotRequired[str]
    """
    Specifies the year month and day on which the individual was born.
    """

    last4_ssn: typing_extensions.NotRequired[str]
    """
    Identifies the last four digits of the government issued (SSN, EIN, TIN).
    """

    masked_account_number: typing_extensions.NotRequired[str]
    """
    Identifies a concealed number associated with the card number recognized by various payment systems. This is typically concealed by storing only the first 6 and/or last 4 digits of the payment account number or some variation.
    """

    payment_tokens: typing_extensions.NotRequired[typing.List[PaymentToken]]
    """
    List of payment tokens for the transaction
    """

    payment_type: typing_extensions.NotRequired[
        typing_extensions.Literal["RECURRING", "TEL", "WEB"]
    ]
    """
    Identifies how accountholders  initiated debits to their accounts .
    """


class _SerializerVerificationAch(pydantic.BaseModel):
    """
    Serializer for VerificationAch handling case conversions
    and file omissions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
        populate_by_name=True,
    )

    account_number: typing.Optional[str] = pydantic.Field(
        alias="accountNumber", default=None
    )
    account_type: typing.Optional[
        typing_extensions.Literal["CHECKING", "CORPORATE_CHECKING", "SAVING"]
    ] = pydantic.Field(alias="accountType", default=None)
    ach_verification_type: typing.Optional[
        typing_extensions.Literal[
            "ACCOUNT_OWNER",
            "ACCOUNT_STATUS",
            "BASIC",
            "PRE_NOTE_CREDIT",
            "PRE_NOTE_DEBIT",
        ]
    ] = pydantic.Field(alias="achVerificationType", default=None)
    consumer_verification_id: typing.Optional[str] = pydantic.Field(
        alias="consumerVerificationId", default=None
    )
    consumer_verification_id_state: typing.Optional[str] = pydantic.Field(
        alias="consumerVerificationIdState", default=None
    )
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
    ecp_program_name: typing.Optional[str] = pydantic.Field(
        alias="ecpProgramName", default=None
    )
    financial_institution_routing_number: typing.Optional[str] = pydantic.Field(
        alias="financialInstitutionRoutingNumber", default=None
    )
    individual_birth_date: typing.Optional[str] = pydantic.Field(
        alias="individualBirthDate", default=None
    )
    last4_ssn: typing.Optional[str] = pydantic.Field(alias="last4SSN", default=None)
    masked_account_number: typing.Optional[str] = pydantic.Field(
        alias="maskedAccountNumber", default=None
    )
    payment_tokens: typing.Optional[typing.List[_SerializerPaymentToken]] = (
        pydantic.Field(alias="paymentTokens", default=None)
    )
    payment_type: typing.Optional[
        typing_extensions.Literal["RECURRING", "TEL", "WEB"]
    ] = pydantic.Field(alias="paymentType", default=None)
