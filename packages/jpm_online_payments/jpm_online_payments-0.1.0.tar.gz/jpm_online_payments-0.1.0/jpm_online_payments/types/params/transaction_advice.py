import typing
import typing_extensions
import pydantic


class TransactionAdvice(typing_extensions.TypedDict):
    """
    Transaction advice information for Amex transaction
    """

    transaction_advice_text: typing_extensions.NotRequired[str]
    """
    Textual information containing Level 3 data for American Express Advice Addendum
    """


class _SerializerTransactionAdvice(pydantic.BaseModel):
    """
    Serializer for TransactionAdvice handling case conversions
    and file omissions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
        populate_by_name=True,
    )

    transaction_advice_text: typing.Optional[str] = pydantic.Field(
        alias="transactionAdviceText", default=None
    )
