import typing
import pydantic


class MerchantSoftware(pydantic.BaseModel):
    """
    Contains information related to the merchant software
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    company_name: str = pydantic.Field(
        alias="companyName",
    )
    """
    Company name of software integrated to this API. If merchant is directly integrated, send "JPMC."
    """
    product_name: str = pydantic.Field(
        alias="productName",
    )
    """
    The name of the product used for marketing purposes from a customer perspective. I. e. what the customer would recognize.
    """
    software_id: typing.Optional[str] = pydantic.Field(alias="softwareId", default=None)
    """
    Unique identifier assigned by Merchant Services at time of integration testing.
    """
    version: typing.Optional[str] = pydantic.Field(alias="version", default=None)
    """
    Designates the unique state of computer software as it is developed and released. The version identifier can be a word, or a number, or both.
    """
