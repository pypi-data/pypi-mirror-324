import typing
import typing_extensions
import pydantic


class RecurringBilling(typing_extensions.TypedDict):
    """
    Partner's Recurring Billing Information
    """

    billing_cycle_sequence_number: typing_extensions.NotRequired[str]
    """
    Identifies the number indicating the location of this record in the sorting sequence of the specified data.
    """

    billing_cycles_total_count: typing_extensions.NotRequired[int]
    """
    Identifies the total number of billing cycles that will be processed when an end date is provided. A billing cycle is a period of time determined by the billing frequency unit and billing frequency count as defined on the recurring plan. In this context, this is the total number of billing cycles expected for the recurring program.
    """

    billing_schedule_update_timestamp: typing_extensions.NotRequired[str]
    """
    Designates the hour, minute, and second in a specific day when the record was last modified.
    """

    initiator_type: typing_extensions.NotRequired[
        typing_extensions.Literal["CARDHOLDER", "MERCHANT"]
    ]
    """
    Describes the initiator of the transaction for the stored credential framework (MIT/CIT)
    """

    payment_frequency_code: typing_extensions.NotRequired[str]
    """
    Codifies the regularity of a set of reoccurring remittances to the firm or another third party (e.g.. Monthly, every 3 months, annually, etc.).
    """


class _SerializerRecurringBilling(pydantic.BaseModel):
    """
    Serializer for RecurringBilling handling case conversions
    and file omissions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
        populate_by_name=True,
    )

    billing_cycle_sequence_number: typing.Optional[str] = pydantic.Field(
        alias="billingCycleSequenceNumber", default=None
    )
    billing_cycles_total_count: typing.Optional[int] = pydantic.Field(
        alias="billingCyclesTotalCount", default=None
    )
    billing_schedule_update_timestamp: typing.Optional[str] = pydantic.Field(
        alias="billingScheduleUpdateTimestamp", default=None
    )
    initiator_type: typing.Optional[
        typing_extensions.Literal["CARDHOLDER", "MERCHANT"]
    ] = pydantic.Field(alias="initiatorType", default=None)
    payment_frequency_code: typing.Optional[str] = pydantic.Field(
        alias="paymentFrequencyCode", default=None
    )
