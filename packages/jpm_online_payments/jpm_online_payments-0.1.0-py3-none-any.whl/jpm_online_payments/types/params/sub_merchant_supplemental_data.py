import typing
import typing_extensions
import pydantic

from .business_information import BusinessInformation, _SerializerBusinessInformation
from .consumer_device import ConsumerDevice, _SerializerConsumerDevice
from .custom_data import CustomData, _SerializerCustomData
from .merchant_identification import (
    MerchantIdentification,
    _SerializerMerchantIdentification,
)
from .merchant_reported_revenue import (
    MerchantReportedRevenue,
    _SerializerMerchantReportedRevenue,
)
from .order_information import OrderInformation, _SerializerOrderInformation
from .partner_service import PartnerService, _SerializerPartnerService
from .recurring_billing import RecurringBilling, _SerializerRecurringBilling
from .address import Address, _SerializerAddress
from .shipping_info import ShippingInfo, _SerializerShippingInfo


class SubMerchantSupplementalData(typing_extensions.TypedDict):
    """
    Additional data provided by merchant for reference purposes.
    """

    business_information: typing_extensions.NotRequired[BusinessInformation]
    """
    Partner's Customer Business information
    """

    consumer_device: typing_extensions.NotRequired[ConsumerDevice]
    """
    Consumer device information provided by merchant
    """

    custom_data: typing_extensions.NotRequired[CustomData]
    """
    Customized data provided by merchant for reference purposes.
    """

    merchant_identification: typing_extensions.NotRequired[MerchantIdentification]
    """
    Sub-Merchant Identification Information
    """

    merchant_reported_revenue: typing_extensions.NotRequired[MerchantReportedRevenue]
    """
    Partner's customer revenue information
    """

    order_information: typing_extensions.NotRequired[OrderInformation]
    """
    Partner's customer order information
    """

    partner_service: typing_extensions.NotRequired[PartnerService]
    """
    Transaction Processing Partner Service Information
    """

    recurring_billing: typing_extensions.NotRequired[RecurringBilling]
    """
    Partner's Recurring Billing Information
    """

    service_address: typing_extensions.NotRequired[Address]
    """
    Address Object
    """

    shipping_info: typing_extensions.NotRequired[ShippingInfo]
    """
    Partner's Shipping Information
    """


class _SerializerSubMerchantSupplementalData(pydantic.BaseModel):
    """
    Serializer for SubMerchantSupplementalData handling case conversions
    and file omissions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
        populate_by_name=True,
    )

    business_information: typing.Optional[_SerializerBusinessInformation] = (
        pydantic.Field(alias="businessInformation", default=None)
    )
    consumer_device: typing.Optional[_SerializerConsumerDevice] = pydantic.Field(
        alias="consumerDevice", default=None
    )
    custom_data: typing.Optional[_SerializerCustomData] = pydantic.Field(
        alias="customData", default=None
    )
    merchant_identification: typing.Optional[_SerializerMerchantIdentification] = (
        pydantic.Field(alias="merchantIdentification", default=None)
    )
    merchant_reported_revenue: typing.Optional[_SerializerMerchantReportedRevenue] = (
        pydantic.Field(alias="merchantReportedRevenue", default=None)
    )
    order_information: typing.Optional[_SerializerOrderInformation] = pydantic.Field(
        alias="orderInformation", default=None
    )
    partner_service: typing.Optional[_SerializerPartnerService] = pydantic.Field(
        alias="partnerService", default=None
    )
    recurring_billing: typing.Optional[_SerializerRecurringBilling] = pydantic.Field(
        alias="recurringBilling", default=None
    )
    service_address: typing.Optional[_SerializerAddress] = pydantic.Field(
        alias="serviceAddress", default=None
    )
    shipping_info: typing.Optional[_SerializerShippingInfo] = pydantic.Field(
        alias="shippingInfo", default=None
    )
