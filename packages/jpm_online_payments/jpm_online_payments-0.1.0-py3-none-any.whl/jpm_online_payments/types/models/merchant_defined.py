import typing
import pydantic


class MerchantDefined(pydantic.BaseModel):
    """
    merchant defined data field that it will pass through to reporting.
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    merchant_defined_data: typing.Optional[str] = pydantic.Field(
        alias="merchantDefinedData", default=None
    )
    """
    Merchant defined data field that pass through to reporting for some endpoints
    """
