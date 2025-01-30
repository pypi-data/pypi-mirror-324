import typing
import typing_extensions
import pydantic

from .payment_token import PaymentToken


class Sepa(pydantic.BaseModel):
    """
    Object for SEPA (Single Euro Payments Area) payment method is a regulatory initiative to facilitate cross border cashless payments across euro-using countries. SEPA allows people doing business across borders in euros to do so with the same ease as domestic transactions within the countries subject to SEPA.
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    international_bank_account_number: str = pydantic.Field(
        alias="internationalBankAccountNumber",
    )
    """
    Identifies the International Bank Account Number (IBAN) for the account.  IBAN is an internationally agreed system of identifying bank accounts across national borders to facilitate the communication and processing of cross border transactions with a reduced risk of transcription errors. Based on ISO 13616 standards, the IBAN consists of up to 34 alphanumeric characters, comprising a country code, two check digits and a long and detailed bank account-number. The check digits enable a sanity check of the bank account number to confirm its integrity before submitting a transaction.
    """
    international_business_identifier_code: str = pydantic.Field(
        alias="internationalBusinessIdentifierCode",
    )
    """
    A valid Bank Identification Code (BIC) according to ISO 9362 standards, that can only contain 8 or 11 alphanumeric characters. Eg: For iDEAL issuer, one of valid BICs is RABONL2U.
    """
    mandate_id: typing.Optional[str] = pydantic.Field(alias="mandateId", default=None)
    """
    Identifies an agreement between the consumer, debtor bank (checking account of the consumer) and the merchant. This agreement (mandate) gives the merchant permission to debit funds from the consumer's checking account for some specific financial purpose (defined by the "Mandate Type"). Typically mandates are used for recurring or installment payments; that is, a fixed amount to be debited over a specific period of time (defined by the ?Mandate Date?). One-time debits are allowed. Mandates are specific to the Singe Euro Payments Area (SEPA) Direct Debit (DD) scheme. SEPA is a system of transactions created by the European Union (EU).
    """
    mandate_signature_date: typing.Optional[str] = pydantic.Field(
        alias="mandateSignatureDate", default=None
    )
    """
    Designates the year, month and day when an agreement between the consumer, debtor bank (checking account of the consumer) and the merchant was signed. This agreement (mandate) gives the merchant permission to debit funds from the consumers checking account for some specific financial purpose. Typically mandates are used for recurring or installment payments; that is, a fixed amount to be debited over a specific period of time (defined by the ?Mandate Date?). One-time debits are allowed. Mandates are specific to the Singe Euro Payments Area (SEPA) Direct Debit (DD) scheme. SEPA is a system of transactions created by the European Union (EU).
    """
    mandate_type: typing.Optional[
        typing_extensions.Literal[
            "CANCEL",
            "CHANGE_TO_ELECTRONIC",
            "FIRST",
            "LAST",
            "NEW",
            "ONE_OFF",
            "RECURRENCE",
        ]
    ] = pydantic.Field(alias="mandateType", default=None)
    """
    Codifies the category an agreement between the consumer, debtor bank (checking account of the consumer) and the merchant. This agreement (mandate) gives the merchant permission to debit funds from the consumers checking account for some specific financial purpose. Typically mandates are used for recurring or installment payments; that is, a fixed amount to be debited over a specific period of time (defined by the ?Mandate Date?). One-time debits are allowed. Mandates are specific to the Singe Euro Payments Area (SEPA) Direct Debit (DD) scheme. SEPA is a system of transactions created by the European Union (EU).
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
    unmasked_account_number: typing.Optional[str] = pydantic.Field(
        alias="unmaskedAccountNumber", default=None
    )
    """
    Identifies a unique occurrence of a payment account.
    """
