import typing
import typing_extensions
import pydantic


class Recurring(typing_extensions.TypedDict):
    """
    Recurring Payment Object
    """

    agreement_id: typing_extensions.NotRequired[str]
    """
    System generated value used to uniquely identify a set of statements presented to the customer whom has acknowledged the acceptance in order to use the online systems.
    """

    is_variable_amount: typing_extensions.NotRequired[bool]
    """
    Identifies the recurring amount as a variable amount rather than a fixed amount.
    """

    payment_agreement_expiry_date: typing_extensions.NotRequired[str]
    """
    Designates the year (YYYY), month (MM), and day (D) at which the agreement with the payer to process payments expires. Used with recurring transaction.
    """

    recurring_sequence: typing_extensions.NotRequired[
        typing_extensions.Literal["FIRST", "SUBSEQUENT"]
    ]
    """
    Identifies whether payment is the first in a series of recurring payments or a subsequent payment. Required for recurring billing.
    """


class _SerializerRecurring(pydantic.BaseModel):
    """
    Serializer for Recurring handling case conversions
    and file omissions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
        populate_by_name=True,
    )

    agreement_id: typing.Optional[str] = pydantic.Field(
        alias="agreementId", default=None
    )
    is_variable_amount: typing.Optional[bool] = pydantic.Field(
        alias="isVariableAmount", default=None
    )
    payment_agreement_expiry_date: typing.Optional[str] = pydantic.Field(
        alias="paymentAgreementExpiryDate", default=None
    )
    recurring_sequence: typing.Optional[
        typing_extensions.Literal["FIRST", "SUBSEQUENT"]
    ] = pydantic.Field(alias="recurringSequence", default=None)
