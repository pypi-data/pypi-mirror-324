import typing
import pydantic


class TapToPay(pydantic.BaseModel):
    """
    Tap To Pay payment information
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    encrypted_payload: typing.Optional[str] = pydantic.Field(
        alias="encryptedPayload", default=None
    )
    """
    Encrypted message details have been rendered unreadable by general means through the application of a given set of instructions and a key.
    """
    reader_id: typing.Optional[str] = pydantic.Field(alias="readerId", default=None)
    """
    Uniquely identifies the reader used for a Tap to Phone transaction.
    """
    transaction_reference_number: typing.Optional[str] = pydantic.Field(
        alias="transactionReferenceNumber", default=None
    )
    """
    Identifies a transaction as assigned by a third-party such as the payment gateway, partner bank, facilitator, aggregator, etc.
    """
