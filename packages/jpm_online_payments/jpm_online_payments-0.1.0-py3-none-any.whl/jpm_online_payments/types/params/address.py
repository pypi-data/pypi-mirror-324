import typing
import typing_extensions
import pydantic


class Address(typing_extensions.TypedDict):
    """
    Address Object
    """

    city: typing_extensions.NotRequired[str]
    """
    Name of municipality.
    """

    country_code: typing_extensions.NotRequired[str]
    """
    The country code of the address based on Alpha 3 ISO standards.
    """

    line1: typing_extensions.NotRequired[str]
    """
    First line of street address.
    """

    line2: typing_extensions.NotRequired[str]
    """
    Second line of street address.
    """

    postal_code: typing_extensions.NotRequired[str]
    """
    The portion of a party?s address that is the encoded representation of a geographic area to facilitate mail delivery services.
    """

    state: typing_extensions.NotRequired[str]
    """
    Name of state or province.
    """


class _SerializerAddress(pydantic.BaseModel):
    """
    Serializer for Address handling case conversions
    and file omissions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
        populate_by_name=True,
    )

    city: typing.Optional[str] = pydantic.Field(alias="city", default=None)
    country_code: typing.Optional[str] = pydantic.Field(
        alias="countryCode", default=None
    )
    line1: typing.Optional[str] = pydantic.Field(alias="line1", default=None)
    line2: typing.Optional[str] = pydantic.Field(alias="line2", default=None)
    postal_code: typing.Optional[str] = pydantic.Field(alias="postalCode", default=None)
    state: typing.Optional[str] = pydantic.Field(alias="state", default=None)
