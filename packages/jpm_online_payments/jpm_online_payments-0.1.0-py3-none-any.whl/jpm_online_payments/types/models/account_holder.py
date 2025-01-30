import typing
import pydantic

from .address import Address
from .consumer_profile_info import ConsumerProfileInfo
from .phone import Phone


class AccountHolder(pydantic.BaseModel):
    """
    Card owner properties
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    ip_address: typing.Optional[str] = pydantic.Field(alias="IPAddress", default=None)
    """
    IP Address from where the transaction is originating
    """
    billing_address: typing.Optional[Address] = pydantic.Field(
        alias="billingAddress", default=None
    )
    """
    Address Object
    """
    consumer_id_creation_date: typing.Optional[str] = pydantic.Field(
        alias="consumerIdCreationDate", default=None
    )
    """
    Designates the century, year, month and day that a merchant's customer profile has been first defined.
    """
    consumer_profile_info: typing.Optional[ConsumerProfileInfo] = pydantic.Field(
        alias="consumerProfileInfo", default=None
    )
    """
    Consumer profile Information if saved
    """
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
    national_id: typing.Optional[str] = pydantic.Field(alias="nationalId", default=None)
    """
    An identifier for the consumer or business assigned by a government authority.
    """
    phone: typing.Optional[Phone] = pydantic.Field(alias="phone", default=None)
    """
    Phone number in ITU-T E.164 format. Country code and phone number (subscriber number) are mandatory values
    """
    reference_id: typing.Optional[str] = pydantic.Field(
        alias="referenceId", default=None
    )
    """
    Merchant defined identifier for a consumer
    """
