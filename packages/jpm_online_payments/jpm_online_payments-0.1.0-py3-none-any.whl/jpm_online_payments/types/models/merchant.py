import typing
import pydantic

from .merchant_software import MerchantSoftware
from .soft_merchant import SoftMerchant


class Merchant(pydantic.BaseModel):
    """
    Information about the merchant
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    location_id: typing.Optional[str] = pydantic.Field(alias="locationId", default=None)
    """
    Identifies the merchant location in which card present transactions are accepted.
    """
    merchant_category_code: typing.Optional[str] = pydantic.Field(
        alias="merchantCategoryCode", default=None
    )
    """
    MCC or Merchant Category Code. Defaults to MCC configured at the merchant profile level. Some configurations allow multiple MCC's under a single Merchant ID. Sending an MCC not configured will result in an error.
    """
    merchant_id: typing.Optional[str] = pydantic.Field(alias="merchantId", default=None)
    """
    Identifier for the merchant account.
    """
    merchant_logo_url: typing.Optional[str] = pydantic.Field(
        alias="merchantLogoUrl", default=None
    )
    """
    Internet address of merchant logo applicable to some alternative payment methods.
    """
    merchant_software: MerchantSoftware = pydantic.Field(
        alias="merchantSoftware",
    )
    """
    Contains information related to the merchant software
    """
    soft_merchant: typing.Optional[SoftMerchant] = pydantic.Field(
        alias="softMerchant", default=None
    )
    """
    Soft merchant information is passed to the card association along with the transaction. This soft merchant information may also be used for cases where smaller businesses or franchise outlets are making a sale in which a merchant aggregator or payment facilitator processes the payment transaction on their behalf.
    """
