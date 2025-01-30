import typing
import pydantic

from .phone import Phone
from .address import Address


class ShipTo(pydantic.BaseModel):
    """
    Object containing information about the recipients
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    email_field: typing.Optional[str] = pydantic.Field(alias="email", default=None)
    """
    Optional value for merchants to provide for a transaction
    """
    first_name: typing.Optional[str] = pydantic.Field(alias="firstName", default=None)
    """
    That part of an individual's full name considered a personal name or given name and generally positioned before the last name or family name.
    """
    full_name: typing.Optional[str] = pydantic.Field(alias="fullName", default=None)
    """
    Name of accountholder
    """
    last_name: typing.Optional[str] = pydantic.Field(alias="lastName", default=None)
    """
    Last name or surname.
    """
    middle_name: typing.Optional[str] = pydantic.Field(alias="middleName", default=None)
    """
    Given name between first name and last name/surname.
    """
    mobile: typing.Optional[Phone] = pydantic.Field(alias="mobile", default=None)
    """
    Phone number in ITU-T E.164 format. Country code and phone number (subscriber number) are mandatory values
    """
    phone: typing.Optional[Phone] = pydantic.Field(alias="phone", default=None)
    """
    Phone number in ITU-T E.164 format. Country code and phone number (subscriber number) are mandatory values
    """
    shipping_address: typing.Optional[Address] = pydantic.Field(
        alias="shippingAddress", default=None
    )
    """
    Address Object
    """
    shipping_description: typing.Optional[str] = pydantic.Field(
        alias="shippingDescription", default=None
    )
    """
    Description of shipping or delivery method
    """
