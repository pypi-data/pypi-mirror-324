import typing
import typing_extensions
import pydantic


class Installment(typing_extensions.TypedDict):
    """
    Object containing information in the file
    """

    installment_count: typing_extensions.NotRequired[int]
    """
    Indicates which payment, out of total number of payments to be made. 
    """

    number_of_deferrals: typing_extensions.NotRequired[int]
    """
    The number of months an installment payment can be postponed or suspended. See documentation for regional requirements.
    """

    plan_id: typing_extensions.NotRequired[str]
    """
    Contains the payment plan identifier.
    """

    total_installments: typing_extensions.NotRequired[int]
    """
    Indicates the total number of installments payments that will be processed.
    """


class _SerializerInstallment(pydantic.BaseModel):
    """
    Serializer for Installment handling case conversions
    and file omissions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
        populate_by_name=True,
    )

    installment_count: typing.Optional[int] = pydantic.Field(
        alias="installmentCount", default=None
    )
    number_of_deferrals: typing.Optional[int] = pydantic.Field(
        alias="numberOfDeferrals", default=None
    )
    plan_id: typing.Optional[str] = pydantic.Field(alias="planId", default=None)
    total_installments: typing.Optional[int] = pydantic.Field(
        alias="totalInstallments", default=None
    )
