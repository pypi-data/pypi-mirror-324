import typing
import typing_extensions
import pydantic

from .verification_ach import VerificationAch, _SerializerVerificationAch
from .verification_card import VerificationCard, _SerializerVerificationCard
from .verification_consumer_profile import (
    VerificationConsumerProfile,
    _SerializerVerificationConsumerProfile,
)
from .verification_sepa import VerificationSepa, _SerializerVerificationSepa


class VerificationPaymentMethodType(typing_extensions.TypedDict):
    """
    Object with one of the payment method type applicable for verification processing
    """

    ach: typing_extensions.NotRequired[VerificationAch]
    """
    Verification of ACH account
    """

    card: typing_extensions.NotRequired[VerificationCard]
    """
    Card payment instrument for card verification
    """

    consumer_profile: typing_extensions.NotRequired[VerificationConsumerProfile]
    """
    Consumer Profile Payment method and attributes needed to process a verification transaction.
    """

    sepa: typing_extensions.NotRequired[VerificationSepa]
    """
    Object for SEPA (Single Euro Payments Area) payment method is a regulatory initiative to facilitate cross border cashless payments across euro-using countries. SEPA allows people doing business across borders in euros to do so with the same ease as domestic transactions within the countries subject to SEPA.
    """


class _SerializerVerificationPaymentMethodType(pydantic.BaseModel):
    """
    Serializer for VerificationPaymentMethodType handling case conversions
    and file omissions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
        populate_by_name=True,
    )

    ach: typing.Optional[_SerializerVerificationAch] = pydantic.Field(
        alias="ach", default=None
    )
    card: typing.Optional[_SerializerVerificationCard] = pydantic.Field(
        alias="card", default=None
    )
    consumer_profile: typing.Optional[_SerializerVerificationConsumerProfile] = (
        pydantic.Field(alias="consumerProfile", default=None)
    )
    sepa: typing.Optional[_SerializerVerificationSepa] = pydantic.Field(
        alias="sepa", default=None
    )
