import typing
import typing_extensions
import pydantic


class Phone(typing_extensions.TypedDict):
    """
    Phone number in ITU-T E.164 format. Country code and phone number (subscriber number) are mandatory values
    """

    country_code: typing_extensions.NotRequired[int]
    """
    Telephone country code.
    """

    phone_number: typing_extensions.Required[str]
    """
    Phone number.
    """


class _SerializerPhone(pydantic.BaseModel):
    """
    Serializer for Phone handling case conversions
    and file omissions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
        populate_by_name=True,
    )

    country_code: typing.Optional[int] = pydantic.Field(
        alias="countryCode", default=None
    )
    phone_number: str = pydantic.Field(
        alias="phoneNumber",
    )
