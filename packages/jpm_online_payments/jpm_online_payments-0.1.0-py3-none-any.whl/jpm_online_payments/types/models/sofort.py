import typing
import pydantic

from .redirected_payment import RedirectedPayment


class Sofort(pydantic.BaseModel):
    """
    Sofort payment method is a single use, delayed notification payment method that requires customers to authenticate their payment
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    bank_name: typing.Optional[str] = pydantic.Field(alias="bankName", default=None)
    """
    The label given to a financial institution authorized by a government to accept deposits, make loans, pay interest, clear checks, and provide other financial services to its customers.
    """
    branch_number: typing.Optional[str] = pydantic.Field(
        alias="branchNumber", default=None
    )
    """
    Uniquely identifies the brick and mortar retail branch location.
    """
    completion_time: typing.Optional[str] = pydantic.Field(
        alias="completionTime", default=None
    )
    """
    Provides a timestamp (UTC). Designates the hour (hh), minute (mm), seconds (ss) and date (if timestamp) or year (YYYY), month (MM), and day (DD) (if date)
    """
    consumer_address_country: typing.Optional[str] = pydantic.Field(
        alias="consumerAddressCountry", default=None
    )
    """
    A code that identifies the Country, a Geographic Area, that is recognized as an independent political unit in world affairs. Note: This data element is a child of the Country Code CDE and valid values are based on ISO standards.
    """
    creation_time: typing.Optional[str] = pydantic.Field(
        alias="creationTime", default=None
    )
    """
    Provides a timestamp (UTC). Designates the hour (hh), minute (mm), seconds (ss) and date (if timestamp) or year (YYYY), month (MM), and day (DD) (if date)
    """
    full_name: typing.Optional[str] = pydantic.Field(alias="fullName", default=None)
    """
    consumerReferenceId
    """
    international_bank_account_number: typing.Optional[str] = pydantic.Field(
        alias="internationalBankAccountNumber", default=None
    )
    """
    Identifies the International Bank Account Number (IBAN) for the account.  IBAN is an internationally agreed system of identifying bank accounts across national borders to facilitate the communication and processing of cross border transactions with a reduced risk of transcription errors. Based on ISO 13616 standards, the IBAN consists of up to 34 alphanumeric characters, comprising a country code, two check digits and a long and detailed bank account-number. The check digits enable a sanity check of the bank account number to confirm its integrity before submitting a transaction.
    """
    international_business_identifier_code: typing.Optional[str] = pydantic.Field(
        alias="internationalBusinessIdentifierCode", default=None
    )
    """
    A valid Bank Identification Code (BIC) according to ISO 9362 standards, that can only contain 8 or 11 alphanumeric characters. Eg: For iDEAL issuer, one of valid BICs is RABONL2U.
    """
    masked_account_number: typing.Optional[str] = pydantic.Field(
        alias="maskedAccountNumber", default=None
    )
    """
    Identifies a concealed number associated with the card number recognized by various payment systems. This is typically concealed by storing only the first 6 and/or last 4 digits of the payment account number or some variation.
    """
    merchant_order_description: typing.Optional[str] = pydantic.Field(
        alias="merchantOrderDescription", default=None
    )
    """
    Merchant provided textual information about the goods and/or services purchased. This text may include details about the prices, quantity and description of goods and/or services to be delivered for all transactions included in the sale.
    """
    preferred_language: typing.Optional[str] = pydantic.Field(
        alias="preferredLanguage", default=None
    )
    """
    Language preference indicated by consumer for pages displayed. Using language tags indicated in RFC5646.
    """
    redirected_payment: typing.Optional[RedirectedPayment] = pydantic.Field(
        alias="redirectedPayment", default=None
    )
    """
    Redirected Payment attributes
    """
