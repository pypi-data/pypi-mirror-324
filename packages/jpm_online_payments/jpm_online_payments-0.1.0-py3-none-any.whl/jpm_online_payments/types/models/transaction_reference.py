import pydantic


class TransactionReference(pydantic.BaseModel):
    """
    Object for refund transaction reference
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    transaction_reference_id: str = pydantic.Field(
        alias="transactionReferenceId",
    )
    """
    Reference to an existing payment.
    """
