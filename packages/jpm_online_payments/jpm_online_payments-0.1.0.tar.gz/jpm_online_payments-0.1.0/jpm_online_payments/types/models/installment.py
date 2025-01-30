import typing
import pydantic


class Installment(pydantic.BaseModel):
    """
    Object containing information in the file
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    installment_count: typing.Optional[int] = pydantic.Field(
        alias="installmentCount", default=None
    )
    """
    Indicates which payment, out of total number of payments to be made. 
    """
    number_of_deferrals: typing.Optional[int] = pydantic.Field(
        alias="numberOfDeferrals", default=None
    )
    """
    The number of months an installment payment can be postponed or suspended. See documentation for regional requirements.
    """
    plan_id: typing.Optional[str] = pydantic.Field(alias="planId", default=None)
    """
    Contains the payment plan identifier.
    """
    total_installments: typing.Optional[int] = pydantic.Field(
        alias="totalInstallments", default=None
    )
    """
    Indicates the total number of installments payments that will be processed.
    """
