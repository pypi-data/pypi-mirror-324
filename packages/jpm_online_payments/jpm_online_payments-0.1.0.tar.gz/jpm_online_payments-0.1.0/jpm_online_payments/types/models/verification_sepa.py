import typing
import typing_extensions
import pydantic

from .payment_token import PaymentToken


class VerificationSepa(pydantic.BaseModel):
    """
    Object for SEPA (Single Euro Payments Area) payment method is a regulatory initiative to facilitate cross border cashless payments across euro-using countries. SEPA allows people doing business across borders in euros to do so with the same ease as domestic transactions within the countries subject to SEPA.
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

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
    payment_tokens: typing.Optional[typing.List[PaymentToken]] = pydantic.Field(
        alias="paymentTokens", default=None
    )
    """
    List of payment tokens for the transaction
    """
    sepa_verification_type: typing.Optional[
        typing_extensions.Literal[
            "ACCOUNT_OWNER",
            "ACCOUNT_STATUS",
            "BASIC",
            "FORWARD_MANDATE",
            "PRE_NOTE_CREDIT",
            "PRE_NOTE_DEBIT",
        ]
    ] = pydantic.Field(alias="sepaVerificationType", default=None)
    """
    Codifies the classification of the payment transaction verification during payment processing which is part if digital safety precaution by sellers to reduce financial risk when handling check payments at point of sale, online or in-person. In this context, this is the verification type for the SEPA transaction.
    """
