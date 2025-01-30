import typing
import pydantic


class TransactionAdvice(pydantic.BaseModel):
    """
    Transaction advice information for Amex transaction
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    transaction_advice_text: typing.Optional[str] = pydantic.Field(
        alias="transactionAdviceText", default=None
    )
    """
    Textual information containing Level 3 data for American Express Advice Addendum
    """
