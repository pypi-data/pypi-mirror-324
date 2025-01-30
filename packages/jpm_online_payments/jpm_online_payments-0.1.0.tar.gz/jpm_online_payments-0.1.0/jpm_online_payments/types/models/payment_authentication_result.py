import typing
import pydantic

from .payment_three_ds_challenge import PaymentThreeDsChallenge
from .payment_three_ds_completion import PaymentThreeDsCompletion
from .three_domain_secure_exemption import ThreeDomainSecureExemption


class PaymentAuthenticationResult(pydantic.BaseModel):
    """
    Cardholder Authentication Result from the Payment request.
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    authentication_id: typing.Optional[str] = pydantic.Field(
        alias="authenticationId", default=None
    )
    """
    Unique identifier for the card owner authentication provided by global authentication solution designed to make eCommerce transactions more secure and reduce fraud.
    """
    authentication_orchestration_url: typing.Optional[str] = pydantic.Field(
        alias="authenticationOrchestrationUrl", default=None
    )
    """
    This is the URL a merchant will need to launch to support 3ds authentication.
    """
    authentication_return_url: typing.Optional[str] = pydantic.Field(
        alias="authenticationReturnUrl", default=None
    )
    """
    Once authentication is complete this is the URL the results where the transaction results will be posted, and where the customer will be redirected. This field must be populated to initiate an authentication.
    """
    three_domain_secure_challenge: typing.Optional[PaymentThreeDsChallenge] = (
        pydantic.Field(alias="threeDomainSecureChallenge", default=None)
    )
    """
    ThreeDS Challenge response from payment call.
    """
    three_domain_secure_completion: typing.Optional[PaymentThreeDsCompletion] = (
        pydantic.Field(alias="threeDomainSecureCompletion", default=None)
    )
    """
    ThreeDS Completion information from payment call.
    """
    three_domain_secure_exemption: typing.Optional[ThreeDomainSecureExemption] = (
        pydantic.Field(alias="threeDomainSecureExemption", default=None)
    )
    """
    Three Domain Secure Closure
    """
    three_domain_secure_server_error_message_text: typing.Optional[str] = (
        pydantic.Field(alias="threeDomainSecureServerErrorMessageText", default=None)
    )
    """
    Provides textual description of a problem that has occurred and is preventing the system from completing a task.
    """
