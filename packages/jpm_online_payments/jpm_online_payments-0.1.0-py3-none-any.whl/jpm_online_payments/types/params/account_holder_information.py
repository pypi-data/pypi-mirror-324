import typing
import typing_extensions
import pydantic

from .address import Address, _SerializerAddress
from .phone import Phone, _SerializerPhone


class AccountHolderInformation(typing_extensions.TypedDict):
    """
    Information about the card Account Holder for which fraud checking is performed.
    """

    address_country_code: typing_extensions.NotRequired[str]
    """
    A code that identifies the Country, a Geographic Area, that is recognized as an independent political unit in world affairs. Note: This data element is a child of the Country Code CDE and valid values are based on ISO standards. In this context, this is the country code of the consumer making the purchase.
    """

    billing_address: typing_extensions.NotRequired[Address]
    """
    Address Object
    """

    birth_date: typing_extensions.NotRequired[str]
    """
    Specifies the year month and day on which the individual was born.
    """

    consumer_id_creation_date: typing_extensions.NotRequired[str]
    """
    Designates the century, year, month and day that a merchant's customer profile has been first defined.
    """

    device_ip_address: typing_extensions.NotRequired[str]
    """
    A unique string of numbers separated by periods that identifies each device using the Internet Protocol (IP) to communicate over a network.  An IP address is assigned to every single computer, printer, switch, router or any other device that is part of a TCP/IP-based network which allows users to send and receive data. The numerals in an IP address are divided into two parts:  1) The network part specifies which networks this address belongs to and 2) The host part further pinpoints the exact location. In this context, this is the IP address of the devices associated with the transaction.
    """

    driver_license_number: typing_extensions.NotRequired[str]
    """
    A unique identifier assigned by a government agency that is not used by a Tax Authority to administer tax laws or by another government body to administer social and government programs. It may be used in conjunction with the party non tax government issued identifier type code. Examples include Driver's License number, green card id, and Passport number.
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

    phone: typing_extensions.NotRequired[Phone]
    """
    Phone number in ITU-T E.164 format. Country code and phone number (subscriber number) are mandatory values
    """

    reference_id: typing_extensions.NotRequired[str]
    """
    Merchant defined identifier for a consumer
    """


class _SerializerAccountHolderInformation(pydantic.BaseModel):
    """
    Serializer for AccountHolderInformation handling case conversions
    and file omissions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
        populate_by_name=True,
    )

    address_country_code: typing.Optional[str] = pydantic.Field(
        alias="addressCountryCode", default=None
    )
    billing_address: typing.Optional[_SerializerAddress] = pydantic.Field(
        alias="billingAddress", default=None
    )
    birth_date: typing.Optional[str] = pydantic.Field(alias="birthDate", default=None)
    consumer_id_creation_date: typing.Optional[str] = pydantic.Field(
        alias="consumerIdCreationDate", default=None
    )
    device_ip_address: typing.Optional[str] = pydantic.Field(
        alias="deviceIPAddress", default=None
    )
    driver_license_number: typing.Optional[str] = pydantic.Field(
        alias="driverLicenseNumber", default=None
    )
    email_field: typing.Optional[str] = pydantic.Field(alias="email", default=None)
    first_name: typing.Optional[str] = pydantic.Field(alias="firstName", default=None)
    full_name: typing.Optional[str] = pydantic.Field(alias="fullName", default=None)
    last_name: typing.Optional[str] = pydantic.Field(alias="lastName", default=None)
    middle_name: typing.Optional[str] = pydantic.Field(alias="middleName", default=None)
    phone: typing.Optional[_SerializerPhone] = pydantic.Field(
        alias="phone", default=None
    )
    reference_id: typing.Optional[str] = pydantic.Field(
        alias="referenceId", default=None
    )
