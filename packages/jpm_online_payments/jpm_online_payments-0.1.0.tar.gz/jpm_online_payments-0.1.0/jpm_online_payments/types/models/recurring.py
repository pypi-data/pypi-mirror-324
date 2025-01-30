import typing
import typing_extensions
import pydantic


class Recurring(pydantic.BaseModel):
    """
    Recurring Payment Object
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    agreement_id: typing.Optional[str] = pydantic.Field(
        alias="agreementId", default=None
    )
    """
    System generated value used to uniquely identify a set of statements presented to the customer whom has acknowledged the acceptance in order to use the online systems.
    """
    is_variable_amount: typing.Optional[bool] = pydantic.Field(
        alias="isVariableAmount", default=None
    )
    """
    Identifies the recurring amount as a variable amount rather than a fixed amount.
    """
    payment_agreement_expiry_date: typing.Optional[str] = pydantic.Field(
        alias="paymentAgreementExpiryDate", default=None
    )
    """
    Designates the year (YYYY), month (MM), and day (D) at which the agreement with the payer to process payments expires. Used with recurring transaction.
    """
    recurring_sequence: typing.Optional[
        typing_extensions.Literal["FIRST", "SUBSEQUENT"]
    ] = pydantic.Field(alias="recurringSequence", default=None)
    """
    Identifies whether payment is the first in a series of recurring payments or a subsequent payment. Required for recurring billing.
    """
