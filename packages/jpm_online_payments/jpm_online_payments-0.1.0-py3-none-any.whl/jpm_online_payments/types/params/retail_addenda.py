import typing
import typing_extensions
import pydantic

from .healthcare_data import HealthcareData, _SerializerHealthcareData
from .level3 import Level3, _SerializerLevel3


class RetailAddenda(typing_extensions.TypedDict):
    """
    Industry-specific attributes.
    """

    gratuity_amount: typing_extensions.NotRequired[int]
    """
    Specifies the monetary value paid by the consumer over and above the payment due for service.
    """

    healthcare_data: typing_extensions.NotRequired[HealthcareData]
    """
    Contains Healthcare qualified transaction information. Amount fields are sub amounts that should be reflected in the total transaction amount.
    """

    is_taxable: typing_extensions.NotRequired[bool]
    """
    Indicates whether tax has been added to the payment.
    """

    level3: typing_extensions.NotRequired[Level3]
    """
    Level 3 data provides commercial shoppers with additional information about purchases on their card statements.
    """

    order_date: typing_extensions.NotRequired[str]
    """
    Designates the year, month, and day the request to purchase a service(s) or good(s) took place.
    """

    purchase_order_number: typing_extensions.NotRequired[str]
    """
    The purchase order number provided by the consumer.
    """

    surcharge_amount: typing_extensions.NotRequired[int]
    """
    Specifies the monetary value of an additional charge by a United States (US) merchant for the customer's usage of the credit card on a domestic US purchase. Surcharging is prohibited outside the US and in several US states and territories. The no-surcharge list currently includes California, Colorado, Connecticut, Florida, Kansas, Maine, Massachusetts, New York, Oklahoma, Texas and Puerto Rico.
    """

    tax_amount: typing_extensions.NotRequired[int]
    """
    Monetary value of the tax amount assessed to the payment.
    """


class _SerializerRetailAddenda(pydantic.BaseModel):
    """
    Serializer for RetailAddenda handling case conversions
    and file omissions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
        populate_by_name=True,
    )

    gratuity_amount: typing.Optional[int] = pydantic.Field(
        alias="gratuityAmount", default=None
    )
    healthcare_data: typing.Optional[_SerializerHealthcareData] = pydantic.Field(
        alias="healthcareData", default=None
    )
    is_taxable: typing.Optional[bool] = pydantic.Field(alias="isTaxable", default=None)
    level3: typing.Optional[_SerializerLevel3] = pydantic.Field(
        alias="level3", default=None
    )
    order_date: typing.Optional[str] = pydantic.Field(alias="orderDate", default=None)
    purchase_order_number: typing.Optional[str] = pydantic.Field(
        alias="purchaseOrderNumber", default=None
    )
    surcharge_amount: typing.Optional[int] = pydantic.Field(
        alias="surchargeAmount", default=None
    )
    tax_amount: typing.Optional[int] = pydantic.Field(alias="taxAmount", default=None)
