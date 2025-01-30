import typing
import typing_extensions
import pydantic


class Mandate(pydantic.BaseModel):
    """
    Agreement information between the consumer, debtor bank (checking account of the consumer) and the merchant for debit funds.
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

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
