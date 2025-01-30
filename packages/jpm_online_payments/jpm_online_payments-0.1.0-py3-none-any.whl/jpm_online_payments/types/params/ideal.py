import typing
import typing_extensions
import pydantic

from .redirected_payment import RedirectedPayment, _SerializerRedirectedPayment


class Ideal(typing_extensions.TypedDict):
    """
    Ideal is Netherland based payment method that allows customers to buy on the Internet using direct online transfers from their bank account.
    """

    completion_time: typing_extensions.NotRequired[str]
    """
    Provides a timestamp (UTC). Designates the hour (hh), minute (mm), seconds (ss) and date (if timestamp) or year (YYYY), month (MM), and day (DD) (if date)
    """

    creation_time: typing_extensions.NotRequired[str]
    """
    Provides a timestamp (UTC). Designates the hour (hh), minute (mm), seconds (ss) and date (if timestamp) or year (YYYY), month (MM), and day (DD) (if date)
    """

    full_name: typing_extensions.NotRequired[str]
    """
    consumerReferenceId
    """

    international_bank_account_number: typing_extensions.NotRequired[str]
    """
    Identifies the International Bank Account Number (IBAN) for the account.  IBAN is an internationally agreed system of identifying bank accounts across national borders to facilitate the communication and processing of cross border transactions with a reduced risk of transcription errors. Based on ISO 13616 standards, the IBAN consists of up to 34 alphanumeric characters, comprising a country code, two check digits and a long and detailed bank account-number. The check digits enable a sanity check of the bank account number to confirm its integrity before submitting a transaction.
    """

    international_business_identifier_code: typing_extensions.NotRequired[str]
    """
    A valid Bank Identification Code (BIC) according to ISO 9362 standards, that can only contain 8 or 11 alphanumeric characters. Eg: For iDEAL issuer, one of valid BICs is RABONL2U.
    """

    merchant_order_description: typing_extensions.NotRequired[str]
    """
    Merchant provided textual information about the goods and/or services purchased. This text may include details about the prices, quantity and description of goods and/or services to be delivered for all transactions included in the sale.
    """

    preferred_language: typing_extensions.NotRequired[str]
    """
    Language preference indicated by consumer for pages displayed. Using language tags indicated in RFC5646.
    """

    redirected_payment: typing_extensions.NotRequired[RedirectedPayment]
    """
    Redirected Payment attributes
    """


class _SerializerIdeal(pydantic.BaseModel):
    """
    Serializer for Ideal handling case conversions
    and file omissions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
        populate_by_name=True,
    )

    completion_time: typing.Optional[str] = pydantic.Field(
        alias="completionTime", default=None
    )
    creation_time: typing.Optional[str] = pydantic.Field(
        alias="creationTime", default=None
    )
    full_name: typing.Optional[str] = pydantic.Field(alias="fullName", default=None)
    international_bank_account_number: typing.Optional[str] = pydantic.Field(
        alias="internationalBankAccountNumber", default=None
    )
    international_business_identifier_code: typing.Optional[str] = pydantic.Field(
        alias="internationalBusinessIdentifierCode", default=None
    )
    merchant_order_description: typing.Optional[str] = pydantic.Field(
        alias="merchantOrderDescription", default=None
    )
    preferred_language: typing.Optional[str] = pydantic.Field(
        alias="preferredLanguage", default=None
    )
    redirected_payment: typing.Optional[_SerializerRedirectedPayment] = pydantic.Field(
        alias="redirectedPayment", default=None
    )
