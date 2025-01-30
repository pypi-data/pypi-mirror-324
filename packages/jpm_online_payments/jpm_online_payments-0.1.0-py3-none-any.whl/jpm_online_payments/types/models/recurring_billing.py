import typing
import typing_extensions
import pydantic


class RecurringBilling(pydantic.BaseModel):
    """
    Partner's Recurring Billing Information
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    billing_cycle_sequence_number: typing.Optional[str] = pydantic.Field(
        alias="billingCycleSequenceNumber", default=None
    )
    """
    Identifies the number indicating the location of this record in the sorting sequence of the specified data.
    """
    billing_cycles_total_count: typing.Optional[int] = pydantic.Field(
        alias="billingCyclesTotalCount", default=None
    )
    """
    Identifies the total number of billing cycles that will be processed when an end date is provided. A billing cycle is a period of time determined by the billing frequency unit and billing frequency count as defined on the recurring plan. In this context, this is the total number of billing cycles expected for the recurring program.
    """
    billing_schedule_update_timestamp: typing.Optional[str] = pydantic.Field(
        alias="billingScheduleUpdateTimestamp", default=None
    )
    """
    Designates the hour, minute, and second in a specific day when the record was last modified.
    """
    initiator_type: typing.Optional[
        typing_extensions.Literal["CARDHOLDER", "MERCHANT"]
    ] = pydantic.Field(alias="initiatorType", default=None)
    """
    Describes the initiator of the transaction for the stored credential framework (MIT/CIT)
    """
    payment_frequency_code: typing.Optional[str] = pydantic.Field(
        alias="paymentFrequencyCode", default=None
    )
    """
    Codifies the regularity of a set of reoccurring remittances to the firm or another third party (e.g.. Monthly, every 3 months, annually, etc.).
    """
