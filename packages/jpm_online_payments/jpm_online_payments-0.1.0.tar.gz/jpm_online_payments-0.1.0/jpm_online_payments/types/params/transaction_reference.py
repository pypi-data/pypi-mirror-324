import typing_extensions
import pydantic


class TransactionReference(typing_extensions.TypedDict):
    """
    Object for refund transaction reference
    """

    transaction_reference_id: typing_extensions.Required[str]
    """
    Reference to an existing payment.
    """


class _SerializerTransactionReference(pydantic.BaseModel):
    """
    Serializer for TransactionReference handling case conversions
    and file omissions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
        populate_by_name=True,
    )

    transaction_reference_id: str = pydantic.Field(
        alias="transactionReferenceId",
    )
