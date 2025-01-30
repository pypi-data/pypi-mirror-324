import typing
import typing_extensions
import pydantic

from .merchant_software import MerchantSoftware, _SerializerMerchantSoftware
from .soft_merchant import SoftMerchant, _SerializerSoftMerchant


class Merchant(typing_extensions.TypedDict):
    """
    Information about the merchant
    """

    location_id: typing_extensions.NotRequired[str]
    """
    Identifies the merchant location in which card present transactions are accepted.
    """

    merchant_category_code: typing_extensions.NotRequired[str]
    """
    MCC or Merchant Category Code. Defaults to MCC configured at the merchant profile level. Some configurations allow multiple MCC's under a single Merchant ID. Sending an MCC not configured will result in an error.
    """

    merchant_id: typing_extensions.NotRequired[str]
    """
    Identifier for the merchant account.
    """

    merchant_logo_url: typing_extensions.NotRequired[str]
    """
    Internet address of merchant logo applicable to some alternative payment methods.
    """

    merchant_software: typing_extensions.Required[MerchantSoftware]
    """
    Contains information related to the merchant software
    """

    soft_merchant: typing_extensions.NotRequired[SoftMerchant]
    """
    Soft merchant information is passed to the card association along with the transaction. This soft merchant information may also be used for cases where smaller businesses or franchise outlets are making a sale in which a merchant aggregator or payment facilitator processes the payment transaction on their behalf.
    """


class _SerializerMerchant(pydantic.BaseModel):
    """
    Serializer for Merchant handling case conversions
    and file omissions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
        populate_by_name=True,
    )

    location_id: typing.Optional[str] = pydantic.Field(alias="locationId", default=None)
    merchant_category_code: typing.Optional[str] = pydantic.Field(
        alias="merchantCategoryCode", default=None
    )
    merchant_id: typing.Optional[str] = pydantic.Field(alias="merchantId", default=None)
    merchant_logo_url: typing.Optional[str] = pydantic.Field(
        alias="merchantLogoUrl", default=None
    )
    merchant_software: _SerializerMerchantSoftware = pydantic.Field(
        alias="merchantSoftware",
    )
    soft_merchant: typing.Optional[_SerializerSoftMerchant] = pydantic.Field(
        alias="softMerchant", default=None
    )
