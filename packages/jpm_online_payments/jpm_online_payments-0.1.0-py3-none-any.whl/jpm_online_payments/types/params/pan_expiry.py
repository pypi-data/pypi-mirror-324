import typing
import typing_extensions
import pydantic


class PanExpiry(typing_extensions.TypedDict):
    """
    Contains expiry for masked PAN if received from network
    """

    month: typing_extensions.NotRequired[int]
    """
    The month of the expiration date
    """

    year: typing_extensions.NotRequired[int]
    """
    The year of the expiration date
    """


class _SerializerPanExpiry(pydantic.BaseModel):
    """
    Serializer for PanExpiry handling case conversions
    and file omissions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
        populate_by_name=True,
    )

    month: typing.Optional[int] = pydantic.Field(alias="month", default=None)
    year: typing.Optional[int] = pydantic.Field(alias="year", default=None)
