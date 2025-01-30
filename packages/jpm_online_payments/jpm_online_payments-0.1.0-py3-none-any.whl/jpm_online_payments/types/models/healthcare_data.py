import typing
import pydantic


class HealthcareData(pydantic.BaseModel):
    """
    Contains Healthcare qualified transaction information. Amount fields are sub amounts that should be reflected in the total transaction amount.
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    is_iias: typing.Optional[bool] = pydantic.Field(alias="isIIAS", default=None)
    """
    Indicates the merchant has implemented an Inventory Information Approval System (IIAS) and used it to get the Total  Healthcare Amount for this transaction.
    """
    total_clinic_amount: typing.Optional[int] = pydantic.Field(
        alias="totalClinicAmount", default=None
    )
    """
    Specifies the total monetary value of qualified clinic and other purchases.
    """
    total_dental_amount: typing.Optional[int] = pydantic.Field(
        alias="totalDentalAmount", default=None
    )
    """
    Specifies the total monetary value of qualified dental purchase.
    """
    total_healthcare_amount: typing.Optional[int] = pydantic.Field(
        alias="totalHealthcareAmount", default=None
    )
    """
    Specifies the total monetary value of qualified healthcare purchases.
    """
    total_prescription_amount: typing.Optional[int] = pydantic.Field(
        alias="totalPrescriptionAmount", default=None
    )
    """
    Specifies the total monetary value of qualified prescription purchases.
    """
    total_vision_amount: typing.Optional[int] = pydantic.Field(
        alias="totalVisionAmount", default=None
    )
    """
    Specifies the total monetary value of qualified vision/optical purchase.
    """
