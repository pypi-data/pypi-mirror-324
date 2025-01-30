import typing
import pydantic


class PanExpiry(pydantic.BaseModel):
    """
    Contains expiry for masked PAN if received from network
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    month: typing.Optional[int] = pydantic.Field(alias="month", default=None)
    """
    The month of the expiration date
    """
    year: typing.Optional[int] = pydantic.Field(alias="year", default=None)
    """
    The year of the expiration date
    """
