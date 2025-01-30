import typing
import pydantic


class Phone(pydantic.BaseModel):
    """
    Phone number in ITU-T E.164 format. Country code and phone number (subscriber number) are mandatory values
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    country_code: typing.Optional[int] = pydantic.Field(
        alias="countryCode", default=None
    )
    """
    Telephone country code.
    """
    phone_number: str = pydantic.Field(
        alias="phoneNumber",
    )
    """
    Phone number.
    """
