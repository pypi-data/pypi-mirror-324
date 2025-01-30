import typing
import typing_extensions
import pydantic


class MerchantDefined(typing_extensions.TypedDict):
    """
    merchant defined data field that it will pass through to reporting.
    """

    merchant_defined_data: typing_extensions.NotRequired[str]
    """
    Merchant defined data field that pass through to reporting for some endpoints
    """


class _SerializerMerchantDefined(pydantic.BaseModel):
    """
    Serializer for MerchantDefined handling case conversions
    and file omissions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
        populate_by_name=True,
    )

    merchant_defined_data: typing.Optional[str] = pydantic.Field(
        alias="merchantDefinedData", default=None
    )
