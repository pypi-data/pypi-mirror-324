import typing
import pydantic

from .verification_ach import VerificationAch
from .verification_card import VerificationCard
from .verification_consumer_profile import VerificationConsumerProfile
from .verification_sepa import VerificationSepa


class VerificationPaymentMethodType(pydantic.BaseModel):
    """
    Object with one of the payment method type applicable for verification processing
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    ach: typing.Optional[VerificationAch] = pydantic.Field(alias="ach", default=None)
    """
    Verification of ACH account
    """
    card: typing.Optional[VerificationCard] = pydantic.Field(alias="card", default=None)
    """
    Card payment instrument for card verification
    """
    consumer_profile: typing.Optional[VerificationConsumerProfile] = pydantic.Field(
        alias="consumerProfile", default=None
    )
    """
    Consumer Profile Payment method and attributes needed to process a verification transaction.
    """
    sepa: typing.Optional[VerificationSepa] = pydantic.Field(alias="sepa", default=None)
    """
    Object for SEPA (Single Euro Payments Area) payment method is a regulatory initiative to facilitate cross border cashless payments across euro-using countries. SEPA allows people doing business across borders in euros to do so with the same ease as domestic transactions within the countries subject to SEPA.
    """
