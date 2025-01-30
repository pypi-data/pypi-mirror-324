import typing
import pydantic


class Address(pydantic.BaseModel):
    """
    Address Object
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    city: typing.Optional[str] = pydantic.Field(alias="city", default=None)
    """
    Name of municipality.
    """
    country_code: typing.Optional[str] = pydantic.Field(
        alias="countryCode", default=None
    )
    """
    The country code of the address based on Alpha 3 ISO standards.
    """
    line1: typing.Optional[str] = pydantic.Field(alias="line1", default=None)
    """
    First line of street address.
    """
    line2: typing.Optional[str] = pydantic.Field(alias="line2", default=None)
    """
    Second line of street address.
    """
    postal_code: typing.Optional[str] = pydantic.Field(alias="postalCode", default=None)
    """
    The portion of a party?s address that is the encoded representation of a geographic area to facilitate mail delivery services.
    """
    state: typing.Optional[str] = pydantic.Field(alias="state", default=None)
    """
    Name of state or province.
    """
