import typing
import pydantic

from .address import Address


class SoftMerchant(pydantic.BaseModel):
    """
    Soft merchant information is passed to the card association along with the transaction. This soft merchant information may also be used for cases where smaller businesses or franchise outlets are making a sale in which a merchant aggregator or payment facilitator processes the payment transaction on their behalf.
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    address: typing.Optional[Address] = pydantic.Field(alias="address", default=None)
    """
    Address Object
    """
    email_field: typing.Optional[str] = pydantic.Field(alias="email", default=None)
    """
    Soft merchant email address
    """
    foreign_merchant_indicator: typing.Optional[bool] = pydantic.Field(
        alias="foreignMerchantIndicator", default=None
    )
    """
    Used to identify a foreign retailer under the Visa Marketplace program
    """
    is_merchant_verification_value_accepted: typing.Optional[bool] = pydantic.Field(
        alias="isMerchantVerificationValueAccepted", default=None
    )
    """
    Identifies if the Merchant Verification Value is accepted by the payment brand.
    """
    master_card_merchant_verification_value_id: typing.Optional[str] = pydantic.Field(
        alias="masterCardMerchantVerificationValueId", default=None
    )
    """
    Identifies the unique number assigned by payment brands to merchants that have registered  to participate in unique interchange programs. Some of the programs that a merchant can register for are the Utility program and the Purchasing Card Large ticket.  Participating in the program allows the merchants to receive a better than priced rate.
    """
    merchant_incorporation_status: typing.Optional[str] = pydantic.Field(
        alias="merchantIncorporationStatus", default=None
    )
    """
    Identifies the incorporation status of the merchant location (6=Tax exempt organizations (501C), 0=Invalid value, blank - Not incorporated (default)).
    """
    merchant_purchase_description: typing.Optional[str] = pydantic.Field(
        alias="merchantPurchaseDescription", default=None
    )
    """
    Description of goods or services sold according to merchant's internal systems.
    """
    name: typing.Optional[str] = pydantic.Field(alias="name", default=None)
    """
    Name of merchant recognizable to account holder intended to be used in the event where the merchant of record is a payment facilitator.
    """
    phone: typing.Optional[str] = pydantic.Field(alias="phone", default=None)
    """
    Soft Merchant phone number
    """
    url: typing.Optional[str] = pydantic.Field(alias="url", default=None)
    """
    Soft merchant URL
    """
    visa_merchant_verification_value_id: typing.Optional[str] = pydantic.Field(
        alias="visaMerchantVerificationValueId", default=None
    )
    """
    Identifies the unique number assigned by payment brands to merchants that have registered  to participate in unique interchange programs. Some of the programs that a merchant can register for are the Utility program and the Purchasing Card Large ticket.  Participating in the program allows the merchants to receive a better than priced rate.
    """
