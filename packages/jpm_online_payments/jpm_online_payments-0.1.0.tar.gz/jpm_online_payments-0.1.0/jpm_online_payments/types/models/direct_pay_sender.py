import typing
import typing_extensions
import pydantic

from .address import Address


class DirectPaySender(pydantic.BaseModel):
    """
    Direct Pay Sender
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    account_number: typing.Optional[str] = pydantic.Field(
        alias="accountNumber", default=None
    )
    """
    The number assigned to a monetary instrument (such as a Card, Direct Debit Account(DDA) or other payment account identifier provided for alternative method of payment or local payment solution) sent to the merchant acquirer to facilitate payment for the exchange of goods and services in a financial transaction. These payment account identifiers can be a secure placeholder such as a Device Primary Account Number(DPAN) or a token or the actual account identifier.
    """
    address: typing.Optional[Address] = pydantic.Field(alias="address", default=None)
    """
    Address Object
    """
    birth_date: typing.Optional[str] = pydantic.Field(alias="birthDate", default=None)
    """
    Specifies the year, month and day on which the individual was born. Format: mmddyyyy
    """
    first_name: typing.Optional[str] = pydantic.Field(alias="firstName", default=None)
    """
    That part of an individual's full name considered a personal name or given name and generally positioned before the last name or family name.
    """
    funding_source: typing.Optional[
        typing_extensions.Literal[
            "CASH",
            "CREDIT_ACCOUNT",
            "CREDIT_CARD",
            "DEBIT_CARD",
            "DEBIT_DEPOSIT_ACCOUNT",
            "MOBILE_MONEY",
            "PREPAID_CARD",
        ]
    ] = pydantic.Field(alias="fundingSource", default=None)
    """
    Codifies the source of the funds that is used in the transaction by the consumer.
    """
    last_name: typing.Optional[str] = pydantic.Field(alias="lastName", default=None)
    """
    Last name or surname.
    """
    middle_name: typing.Optional[str] = pydantic.Field(alias="middleName", default=None)
    """
    Given name between first name and last name/surname.
    """
    tax_id: typing.Optional[str] = pydantic.Field(alias="taxId", default=None)
    """
    An identifier assigned by a government agency that is used by a Tax Authority to administer tax laws or by another government body to administer social and government programs.
    """
    tax_id_type: typing.Optional[typing_extensions.Literal["EIN", "ITIN", "SSN"]] = (
        pydantic.Field(alias="taxIdType", default=None)
    )
    """
    A code that classifies the type of Tax Government Identifier.
    """
    transaction_reference_number: typing.Optional[str] = pydantic.Field(
        alias="transactionReferenceNumber", default=None
    )
    """
    Identifies a transaction as assigned by a third-party such as the payment gateway, partner bank, facilitator, aggregator, etc.
    """
