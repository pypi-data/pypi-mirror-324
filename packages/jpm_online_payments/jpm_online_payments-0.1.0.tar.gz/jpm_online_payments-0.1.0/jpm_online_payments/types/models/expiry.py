import pydantic


class Expiry(pydantic.BaseModel):
    """
    Expiration date
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    month: int = pydantic.Field(
        alias="month",
    )
    """
    The month of the expiration date
    """
    year: int = pydantic.Field(
        alias="year",
    )
    """
    The year of the expiration date
    """
