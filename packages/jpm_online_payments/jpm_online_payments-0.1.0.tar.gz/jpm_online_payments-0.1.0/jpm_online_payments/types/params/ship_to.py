import typing
import typing_extensions
import pydantic

from .phone import Phone, _SerializerPhone
from .address import Address, _SerializerAddress


class ShipTo(typing_extensions.TypedDict):
    """
    Object containing information about the recipients
    """

    email_field: typing_extensions.NotRequired[str]
    """
    Optional value for merchants to provide for a transaction
    """

    first_name: typing_extensions.NotRequired[str]
    """
    That part of an individual's full name considered a personal name or given name and generally positioned before the last name or family name.
    """

    full_name: typing_extensions.NotRequired[str]
    """
    Name of accountholder
    """

    last_name: typing_extensions.NotRequired[str]
    """
    Last name or surname.
    """

    middle_name: typing_extensions.NotRequired[str]
    """
    Given name between first name and last name/surname.
    """

    mobile: typing_extensions.NotRequired[Phone]
    """
    Phone number in ITU-T E.164 format. Country code and phone number (subscriber number) are mandatory values
    """

    phone: typing_extensions.NotRequired[Phone]
    """
    Phone number in ITU-T E.164 format. Country code and phone number (subscriber number) are mandatory values
    """

    shipping_address: typing_extensions.NotRequired[Address]
    """
    Address Object
    """

    shipping_description: typing_extensions.NotRequired[str]
    """
    Description of shipping or delivery method
    """


class _SerializerShipTo(pydantic.BaseModel):
    """
    Serializer for ShipTo handling case conversions
    and file omissions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
        populate_by_name=True,
    )

    email_field: typing.Optional[str] = pydantic.Field(alias="email", default=None)
    first_name: typing.Optional[str] = pydantic.Field(alias="firstName", default=None)
    full_name: typing.Optional[str] = pydantic.Field(alias="fullName", default=None)
    last_name: typing.Optional[str] = pydantic.Field(alias="lastName", default=None)
    middle_name: typing.Optional[str] = pydantic.Field(alias="middleName", default=None)
    mobile: typing.Optional[_SerializerPhone] = pydantic.Field(
        alias="mobile", default=None
    )
    phone: typing.Optional[_SerializerPhone] = pydantic.Field(
        alias="phone", default=None
    )
    shipping_address: typing.Optional[_SerializerAddress] = pydantic.Field(
        alias="shippingAddress", default=None
    )
    shipping_description: typing.Optional[str] = pydantic.Field(
        alias="shippingDescription", default=None
    )
