import typing
import typing_extensions
import pydantic

from .address import Address, _SerializerAddress
from .consumer_profile_info import ConsumerProfileInfo, _SerializerConsumerProfileInfo
from .phone import Phone, _SerializerPhone


class AccountHolder(typing_extensions.TypedDict):
    """
    Card owner properties
    """

    ip_address: typing_extensions.NotRequired[str]
    """
    IP Address from where the transaction is originating
    """

    billing_address: typing_extensions.NotRequired[Address]
    """
    Address Object
    """

    consumer_id_creation_date: typing_extensions.NotRequired[str]
    """
    Designates the century, year, month and day that a merchant's customer profile has been first defined.
    """

    consumer_profile_info: typing_extensions.NotRequired[ConsumerProfileInfo]
    """
    Consumer profile Information if saved
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

    national_id: typing_extensions.NotRequired[str]
    """
    An identifier for the consumer or business assigned by a government authority.
    """

    phone: typing_extensions.NotRequired[Phone]
    """
    Phone number in ITU-T E.164 format. Country code and phone number (subscriber number) are mandatory values
    """

    reference_id: typing_extensions.NotRequired[str]
    """
    Merchant defined identifier for a consumer
    """


class _SerializerAccountHolder(pydantic.BaseModel):
    """
    Serializer for AccountHolder handling case conversions
    and file omissions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
        populate_by_name=True,
    )

    ip_address: typing.Optional[str] = pydantic.Field(alias="IPAddress", default=None)
    billing_address: typing.Optional[_SerializerAddress] = pydantic.Field(
        alias="billingAddress", default=None
    )
    consumer_id_creation_date: typing.Optional[str] = pydantic.Field(
        alias="consumerIdCreationDate", default=None
    )
    consumer_profile_info: typing.Optional[_SerializerConsumerProfileInfo] = (
        pydantic.Field(alias="consumerProfileInfo", default=None)
    )
    email_field: typing.Optional[str] = pydantic.Field(alias="email", default=None)
    first_name: typing.Optional[str] = pydantic.Field(alias="firstName", default=None)
    full_name: typing.Optional[str] = pydantic.Field(alias="fullName", default=None)
    last_name: typing.Optional[str] = pydantic.Field(alias="lastName", default=None)
    middle_name: typing.Optional[str] = pydantic.Field(alias="middleName", default=None)
    mobile: typing.Optional[_SerializerPhone] = pydantic.Field(
        alias="mobile", default=None
    )
    national_id: typing.Optional[str] = pydantic.Field(alias="nationalId", default=None)
    phone: typing.Optional[_SerializerPhone] = pydantic.Field(
        alias="phone", default=None
    )
    reference_id: typing.Optional[str] = pydantic.Field(
        alias="referenceId", default=None
    )
