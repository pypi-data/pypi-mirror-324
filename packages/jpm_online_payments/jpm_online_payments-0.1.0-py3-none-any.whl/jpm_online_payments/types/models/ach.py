import typing
import typing_extensions
import pydantic

from .payment_token import PaymentToken


class Ach(pydantic.BaseModel):
    """
    Object for ACH (Automated Clearing House) payment method which occurs whenever someone instructs the ACH network to ?push? money from their account to someone else's. This is mostly used in USA.
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    account_number: str = pydantic.Field(
        alias="accountNumber",
    )
    """
    The card or token number.
    """
    account_type: typing.Optional[
        typing_extensions.Literal["CHECKING", "CORPORATE_CHECKING", "SAVING"]
    ] = pydantic.Field(alias="accountType", default=None)
    """
    Type of banking account.
    """
    ecp_program_name: typing.Optional[str] = pydantic.Field(
        alias="ecpProgramName", default=None
    )
    """
    Label of the program used for backend processing when handling electronic or paper checks at point of sale, online or in-person.
    """
    financial_institution_routing_number: typing.Optional[str] = pydantic.Field(
        alias="financialInstitutionRoutingNumber", default=None
    )
    """
    Identifies the routing and transit number. In the United  States it's 8-9 numeric characters.
    """
    is_transaction_micro_entry: typing.Optional[bool] = pydantic.Field(
        alias="isTransactionMicroEntry", default=None
    )
    """
    Indicates If a Micro-Entry  is used for account validation purposes. *Micro-Entries are defined as ACH credits of less than $1 and any offsetting ACH debits to verify a Receiver?s account.
    """
    masked_account_number: typing.Optional[str] = pydantic.Field(
        alias="maskedAccountNumber", default=None
    )
    """
    Identifies a concealed number associated with the card number recognized by various payment systems. This is typically concealed by storing only the first 6 and/or last 4 digits of the payment account number or some variation.
    """
    payment_tokens: typing.Optional[typing.List[PaymentToken]] = pydantic.Field(
        alias="paymentTokens", default=None
    )
    """
    List of payment tokens for the transaction
    """
    payment_type: typing.Optional[
        typing_extensions.Literal["RECURRING", "TEL", "WEB"]
    ] = pydantic.Field(alias="paymentType", default=None)
    """
    Identifies how accountholders  initiated debits to their accounts .
    """
    unmasked_account_number: typing.Optional[str] = pydantic.Field(
        alias="unmaskedAccountNumber", default=None
    )
    """
    Identifies a unique occurrence of a payment account.
    """
