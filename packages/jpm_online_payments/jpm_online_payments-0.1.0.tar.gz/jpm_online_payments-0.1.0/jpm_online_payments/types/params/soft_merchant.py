import typing
import typing_extensions
import pydantic

from .address import Address, _SerializerAddress


class SoftMerchant(typing_extensions.TypedDict):
    """
    Soft merchant information is passed to the card association along with the transaction. This soft merchant information may also be used for cases where smaller businesses or franchise outlets are making a sale in which a merchant aggregator or payment facilitator processes the payment transaction on their behalf.
    """

    address: typing_extensions.NotRequired[Address]
    """
    Address Object
    """

    email_field: typing_extensions.NotRequired[str]
    """
    Soft merchant email address
    """

    foreign_merchant_indicator: typing_extensions.NotRequired[bool]
    """
    Used to identify a foreign retailer under the Visa Marketplace program
    """

    is_merchant_verification_value_accepted: typing_extensions.NotRequired[bool]
    """
    Identifies if the Merchant Verification Value is accepted by the payment brand.
    """

    master_card_merchant_verification_value_id: typing_extensions.NotRequired[str]
    """
    Identifies the unique number assigned by payment brands to merchants that have registered  to participate in unique interchange programs. Some of the programs that a merchant can register for are the Utility program and the Purchasing Card Large ticket.  Participating in the program allows the merchants to receive a better than priced rate.
    """

    merchant_incorporation_status: typing_extensions.NotRequired[str]
    """
    Identifies the incorporation status of the merchant location (6=Tax exempt organizations (501C), 0=Invalid value, blank - Not incorporated (default)).
    """

    merchant_purchase_description: typing_extensions.NotRequired[str]
    """
    Description of goods or services sold according to merchant's internal systems.
    """

    name: typing_extensions.NotRequired[str]
    """
    Name of merchant recognizable to account holder intended to be used in the event where the merchant of record is a payment facilitator.
    """

    phone: typing_extensions.NotRequired[str]
    """
    Soft Merchant phone number
    """

    url: typing_extensions.NotRequired[str]
    """
    Soft merchant URL
    """

    visa_merchant_verification_value_id: typing_extensions.NotRequired[str]
    """
    Identifies the unique number assigned by payment brands to merchants that have registered  to participate in unique interchange programs. Some of the programs that a merchant can register for are the Utility program and the Purchasing Card Large ticket.  Participating in the program allows the merchants to receive a better than priced rate.
    """


class _SerializerSoftMerchant(pydantic.BaseModel):
    """
    Serializer for SoftMerchant handling case conversions
    and file omissions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
        populate_by_name=True,
    )

    address: typing.Optional[_SerializerAddress] = pydantic.Field(
        alias="address", default=None
    )
    email_field: typing.Optional[str] = pydantic.Field(alias="email", default=None)
    foreign_merchant_indicator: typing.Optional[bool] = pydantic.Field(
        alias="foreignMerchantIndicator", default=None
    )
    is_merchant_verification_value_accepted: typing.Optional[bool] = pydantic.Field(
        alias="isMerchantVerificationValueAccepted", default=None
    )
    master_card_merchant_verification_value_id: typing.Optional[str] = pydantic.Field(
        alias="masterCardMerchantVerificationValueId", default=None
    )
    merchant_incorporation_status: typing.Optional[str] = pydantic.Field(
        alias="merchantIncorporationStatus", default=None
    )
    merchant_purchase_description: typing.Optional[str] = pydantic.Field(
        alias="merchantPurchaseDescription", default=None
    )
    name: typing.Optional[str] = pydantic.Field(alias="name", default=None)
    phone: typing.Optional[str] = pydantic.Field(alias="phone", default=None)
    url: typing.Optional[str] = pydantic.Field(alias="url", default=None)
    visa_merchant_verification_value_id: typing.Optional[str] = pydantic.Field(
        alias="visaMerchantVerificationValueId", default=None
    )
