import typing
import pydantic

from .business_information import BusinessInformation
from .consumer_device import ConsumerDevice
from .custom_data import CustomData
from .merchant_identification import MerchantIdentification
from .merchant_reported_revenue import MerchantReportedRevenue
from .order_information import OrderInformation
from .partner_service import PartnerService
from .recurring_billing import RecurringBilling
from .address import Address
from .shipping_info import ShippingInfo


class SubMerchantSupplementalData(pydantic.BaseModel):
    """
    Additional data provided by merchant for reference purposes.
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    business_information: typing.Optional[BusinessInformation] = pydantic.Field(
        alias="businessInformation", default=None
    )
    """
    Partner's Customer Business information
    """
    consumer_device: typing.Optional[ConsumerDevice] = pydantic.Field(
        alias="consumerDevice", default=None
    )
    """
    Consumer device information provided by merchant
    """
    custom_data: typing.Optional[CustomData] = pydantic.Field(
        alias="customData", default=None
    )
    """
    Customized data provided by merchant for reference purposes.
    """
    merchant_identification: typing.Optional[MerchantIdentification] = pydantic.Field(
        alias="merchantIdentification", default=None
    )
    """
    Sub-Merchant Identification Information
    """
    merchant_reported_revenue: typing.Optional[MerchantReportedRevenue] = (
        pydantic.Field(alias="merchantReportedRevenue", default=None)
    )
    """
    Partner's customer revenue information
    """
    order_information: typing.Optional[OrderInformation] = pydantic.Field(
        alias="orderInformation", default=None
    )
    """
    Partner's customer order information
    """
    partner_service: typing.Optional[PartnerService] = pydantic.Field(
        alias="partnerService", default=None
    )
    """
    Transaction Processing Partner Service Information
    """
    recurring_billing: typing.Optional[RecurringBilling] = pydantic.Field(
        alias="recurringBilling", default=None
    )
    """
    Partner's Recurring Billing Information
    """
    service_address: typing.Optional[Address] = pydantic.Field(
        alias="serviceAddress", default=None
    )
    """
    Address Object
    """
    shipping_info: typing.Optional[ShippingInfo] = pydantic.Field(
        alias="shippingInfo", default=None
    )
    """
    Partner's Shipping Information
    """
