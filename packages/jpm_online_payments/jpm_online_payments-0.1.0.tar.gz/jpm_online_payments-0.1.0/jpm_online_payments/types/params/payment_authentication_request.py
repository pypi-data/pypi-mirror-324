import typing
import typing_extensions
import pydantic

from .payment_three_ds_account_additional_info import (
    PaymentThreeDsAccountAdditionalInfo,
    _SerializerPaymentThreeDsAccountAdditionalInfo,
)
from .three_ds_message_extension import (
    ThreeDsMessageExtension,
    _SerializerThreeDsMessageExtension,
)
from .payment_three_ds_purchase_info import (
    PaymentThreeDsPurchaseInfo,
    _SerializerPaymentThreeDsPurchaseInfo,
)
from .three_ds_purchase_risk import ThreeDsPurchaseRisk, _SerializerThreeDsPurchaseRisk
from .three_ds_requestor_authentication_info import (
    ThreeDsRequestorAuthenticationInfo,
    _SerializerThreeDsRequestorAuthenticationInfo,
)
from .three_ds_requestor_prior_authentication_info import (
    ThreeDsRequestorPriorAuthenticationInfo,
    _SerializerThreeDsRequestorPriorAuthenticationInfo,
)


class PaymentAuthenticationRequest(typing_extensions.TypedDict):
    """
    Request Authentication during payment process
    """

    account_type: typing_extensions.NotRequired[
        typing_extensions.Literal["CREDIT", "DEBIT", "JCB_PREPAID", "NOT_APPLICABLE"]
    ]
    """
    Indicates the type of consumer account is requested for authentication.
    """

    authentication_return_url: typing_extensions.NotRequired[str]
    """
    Once authentication is complete this is the URL the results where the transaction results will be posted, and where the customer will be redirected. This field must be populated to initiate an authentication.
    """

    authentication_support_url: typing_extensions.NotRequired[str]
    """
    Fully qualified URL of the 3DS Requestor website or customer care site. Provides additional information to the receiving 3D Secure system if a problem arises and should provide a contact information.
    """

    authentication_type: typing_extensions.NotRequired[
        typing_extensions.Literal["AUTHENTICATION", "DEFAULT", "EXEMPTION"]
    ]
    """
    Indicates the type of cardholder Authentication request requested by the authentication requestor.
    """

    three_ds_account_additional_info: typing_extensions.NotRequired[
        PaymentThreeDsAccountAdditionalInfo
    ]
    """
    Additional account  Information used for authentication processing.
    """

    three_ds_message_extensions: typing_extensions.NotRequired[
        typing.List[ThreeDsMessageExtension]
    ]
    """
    List of Three DS Message Extension information
    """

    three_ds_purchase_info: typing_extensions.NotRequired[PaymentThreeDsPurchaseInfo]
    """
    Three DS Purchase Information for the payment request
    """

    three_ds_purchase_risk: typing_extensions.NotRequired[ThreeDsPurchaseRisk]
    """
    Contains Risk related information provided by the  3DS Requestor.
    """

    three_ds_requestor_authentication_info: typing_extensions.NotRequired[
        ThreeDsRequestorAuthenticationInfo
    ]
    """
    Information about how the 3DS Requestor authenticated the cardholder before or during the transaction.
    """

    three_ds_requestor_prior_authentication_info: typing_extensions.NotRequired[
        ThreeDsRequestorPriorAuthenticationInfo
    ]
    """
    Contains information about how the 3DS Requestor authenticated the cardholder as part of a previous 3DS transaction.
    """


class _SerializerPaymentAuthenticationRequest(pydantic.BaseModel):
    """
    Serializer for PaymentAuthenticationRequest handling case conversions
    and file omissions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
        populate_by_name=True,
    )

    account_type: typing.Optional[
        typing_extensions.Literal["CREDIT", "DEBIT", "JCB_PREPAID", "NOT_APPLICABLE"]
    ] = pydantic.Field(alias="accountType", default=None)
    authentication_return_url: typing.Optional[str] = pydantic.Field(
        alias="authenticationReturnUrl", default=None
    )
    authentication_support_url: typing.Optional[str] = pydantic.Field(
        alias="authenticationSupportUrl", default=None
    )
    authentication_type: typing.Optional[
        typing_extensions.Literal["AUTHENTICATION", "DEFAULT", "EXEMPTION"]
    ] = pydantic.Field(alias="authenticationType", default=None)
    three_ds_account_additional_info: typing.Optional[
        _SerializerPaymentThreeDsAccountAdditionalInfo
    ] = pydantic.Field(alias="threeDSAccountAdditionalInfo", default=None)
    three_ds_message_extensions: typing.Optional[
        typing.List[_SerializerThreeDsMessageExtension]
    ] = pydantic.Field(alias="threeDSMessageExtensions", default=None)
    three_ds_purchase_info: typing.Optional[_SerializerPaymentThreeDsPurchaseInfo] = (
        pydantic.Field(alias="threeDSPurchaseInfo", default=None)
    )
    three_ds_purchase_risk: typing.Optional[_SerializerThreeDsPurchaseRisk] = (
        pydantic.Field(alias="threeDSPurchaseRisk", default=None)
    )
    three_ds_requestor_authentication_info: typing.Optional[
        _SerializerThreeDsRequestorAuthenticationInfo
    ] = pydantic.Field(alias="threeDSRequestorAuthenticationInfo", default=None)
    three_ds_requestor_prior_authentication_info: typing.Optional[
        _SerializerThreeDsRequestorPriorAuthenticationInfo
    ] = pydantic.Field(alias="threeDSRequestorPriorAuthenticationInfo", default=None)
