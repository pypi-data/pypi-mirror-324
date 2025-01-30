import typing_extensions
import pydantic


class Expiry(typing_extensions.TypedDict):
    """
    Expiration date
    """

    month: typing_extensions.Required[int]
    """
    The month of the expiration date
    """

    year: typing_extensions.Required[int]
    """
    The year of the expiration date
    """


class _SerializerExpiry(pydantic.BaseModel):
    """
    Serializer for Expiry handling case conversions
    and file omissions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
        populate_by_name=True,
    )

    month: int = pydantic.Field(
        alias="month",
    )
    year: int = pydantic.Field(
        alias="year",
    )
