import typing
import typing_extensions
import pydantic


class MerchantSoftware(typing_extensions.TypedDict):
    """
    Contains information related to the merchant software
    """

    company_name: typing_extensions.Required[str]
    """
    Company name of software integrated to this API. If merchant is directly integrated, send "JPMC."
    """

    product_name: typing_extensions.Required[str]
    """
    The name of the product used for marketing purposes from a customer perspective. I. e. what the customer would recognize.
    """

    software_id: typing_extensions.NotRequired[str]
    """
    Unique identifier assigned by Merchant Services at time of integration testing.
    """

    version: typing_extensions.NotRequired[str]
    """
    Designates the unique state of computer software as it is developed and released. The version identifier can be a word, or a number, or both.
    """


class _SerializerMerchantSoftware(pydantic.BaseModel):
    """
    Serializer for MerchantSoftware handling case conversions
    and file omissions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
        populate_by_name=True,
    )

    company_name: str = pydantic.Field(
        alias="companyName",
    )
    product_name: str = pydantic.Field(
        alias="productName",
    )
    software_id: typing.Optional[str] = pydantic.Field(alias="softwareId", default=None)
    version: typing.Optional[str] = pydantic.Field(alias="version", default=None)
