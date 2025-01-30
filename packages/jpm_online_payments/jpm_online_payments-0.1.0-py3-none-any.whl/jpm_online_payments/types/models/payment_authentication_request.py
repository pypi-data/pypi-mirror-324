import typing
import typing_extensions
import pydantic

from .payment_three_ds_account_additional_info import (
    PaymentThreeDsAccountAdditionalInfo,
)
from .three_ds_message_extension import ThreeDsMessageExtension
from .payment_three_ds_purchase_info import PaymentThreeDsPurchaseInfo
from .three_ds_purchase_risk import ThreeDsPurchaseRisk
from .three_ds_requestor_authentication_info import ThreeDsRequestorAuthenticationInfo
from .three_ds_requestor_prior_authentication_info import (
    ThreeDsRequestorPriorAuthenticationInfo,
)


class PaymentAuthenticationRequest(pydantic.BaseModel):
    """
    Request Authentication during payment process
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    account_type: typing.Optional[
        typing_extensions.Literal["CREDIT", "DEBIT", "JCB_PREPAID", "NOT_APPLICABLE"]
    ] = pydantic.Field(alias="accountType", default=None)
    """
    Indicates the type of consumer account is requested for authentication.
    """
    authentication_return_url: typing.Optional[str] = pydantic.Field(
        alias="authenticationReturnUrl", default=None
    )
    """
    Once authentication is complete this is the URL the results where the transaction results will be posted, and where the customer will be redirected. This field must be populated to initiate an authentication.
    """
    authentication_support_url: typing.Optional[str] = pydantic.Field(
        alias="authenticationSupportUrl", default=None
    )
    """
    Fully qualified URL of the 3DS Requestor website or customer care site. Provides additional information to the receiving 3D Secure system if a problem arises and should provide a contact information.
    """
    authentication_type: typing.Optional[
        typing_extensions.Literal["AUTHENTICATION", "DEFAULT", "EXEMPTION"]
    ] = pydantic.Field(alias="authenticationType", default=None)
    """
    Indicates the type of cardholder Authentication request requested by the authentication requestor.
    """
    three_ds_account_additional_info: typing.Optional[
        PaymentThreeDsAccountAdditionalInfo
    ] = pydantic.Field(alias="threeDSAccountAdditionalInfo", default=None)
    """
    Additional account  Information used for authentication processing.
    """
    three_ds_message_extensions: typing.Optional[
        typing.List[ThreeDsMessageExtension]
    ] = pydantic.Field(alias="threeDSMessageExtensions", default=None)
    """
    List of Three DS Message Extension information
    """
    three_ds_purchase_info: typing.Optional[PaymentThreeDsPurchaseInfo] = (
        pydantic.Field(alias="threeDSPurchaseInfo", default=None)
    )
    """
    Three DS Purchase Information for the payment request
    """
    three_ds_purchase_risk: typing.Optional[ThreeDsPurchaseRisk] = pydantic.Field(
        alias="threeDSPurchaseRisk", default=None
    )
    """
    Contains Risk related information provided by the  3DS Requestor.
    """
    three_ds_requestor_authentication_info: typing.Optional[
        ThreeDsRequestorAuthenticationInfo
    ] = pydantic.Field(alias="threeDSRequestorAuthenticationInfo", default=None)
    """
    Information about how the 3DS Requestor authenticated the cardholder before or during the transaction.
    """
    three_ds_requestor_prior_authentication_info: typing.Optional[
        ThreeDsRequestorPriorAuthenticationInfo
    ] = pydantic.Field(alias="threeDSRequestorPriorAuthenticationInfo", default=None)
    """
    Contains information about how the 3DS Requestor authenticated the cardholder as part of a previous 3DS transaction.
    """
