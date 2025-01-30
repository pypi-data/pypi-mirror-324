import typing
import typing_extensions
import pydantic


class TapToPay(typing_extensions.TypedDict):
    """
    Tap To Pay payment information
    """

    encrypted_payload: typing_extensions.NotRequired[str]
    """
    Encrypted message details have been rendered unreadable by general means through the application of a given set of instructions and a key.
    """

    reader_id: typing_extensions.NotRequired[str]
    """
    Uniquely identifies the reader used for a Tap to Phone transaction.
    """

    transaction_reference_number: typing_extensions.NotRequired[str]
    """
    Identifies a transaction as assigned by a third-party such as the payment gateway, partner bank, facilitator, aggregator, etc.
    """


class _SerializerTapToPay(pydantic.BaseModel):
    """
    Serializer for TapToPay handling case conversions
    and file omissions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
        populate_by_name=True,
    )

    encrypted_payload: typing.Optional[str] = pydantic.Field(
        alias="encryptedPayload", default=None
    )
    reader_id: typing.Optional[str] = pydantic.Field(alias="readerId", default=None)
    transaction_reference_number: typing.Optional[str] = pydantic.Field(
        alias="transactionReferenceNumber", default=None
    )
