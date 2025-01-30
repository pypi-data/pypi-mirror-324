import typing
import typing_extensions
import pydantic


class HealthcareData(typing_extensions.TypedDict):
    """
    Contains Healthcare qualified transaction information. Amount fields are sub amounts that should be reflected in the total transaction amount.
    """

    is_iias: typing_extensions.NotRequired[bool]
    """
    Indicates the merchant has implemented an Inventory Information Approval System (IIAS) and used it to get the Total  Healthcare Amount for this transaction.
    """

    total_clinic_amount: typing_extensions.NotRequired[int]
    """
    Specifies the total monetary value of qualified clinic and other purchases.
    """

    total_dental_amount: typing_extensions.NotRequired[int]
    """
    Specifies the total monetary value of qualified dental purchase.
    """

    total_healthcare_amount: typing_extensions.NotRequired[int]
    """
    Specifies the total monetary value of qualified healthcare purchases.
    """

    total_prescription_amount: typing_extensions.NotRequired[int]
    """
    Specifies the total monetary value of qualified prescription purchases.
    """

    total_vision_amount: typing_extensions.NotRequired[int]
    """
    Specifies the total monetary value of qualified vision/optical purchase.
    """


class _SerializerHealthcareData(pydantic.BaseModel):
    """
    Serializer for HealthcareData handling case conversions
    and file omissions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
        populate_by_name=True,
    )

    is_iias: typing.Optional[bool] = pydantic.Field(alias="isIIAS", default=None)
    total_clinic_amount: typing.Optional[int] = pydantic.Field(
        alias="totalClinicAmount", default=None
    )
    total_dental_amount: typing.Optional[int] = pydantic.Field(
        alias="totalDentalAmount", default=None
    )
    total_healthcare_amount: typing.Optional[int] = pydantic.Field(
        alias="totalHealthcareAmount", default=None
    )
    total_prescription_amount: typing.Optional[int] = pydantic.Field(
        alias="totalPrescriptionAmount", default=None
    )
    total_vision_amount: typing.Optional[int] = pydantic.Field(
        alias="totalVisionAmount", default=None
    )
