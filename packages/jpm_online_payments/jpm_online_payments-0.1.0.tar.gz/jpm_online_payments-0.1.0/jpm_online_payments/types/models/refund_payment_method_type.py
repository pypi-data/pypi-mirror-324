import typing
import pydantic

from .ach import Ach
from .refund_card import RefundCard
from .refund_consumer_profile import RefundConsumerProfile
from .sepa import Sepa
from .tap_to_pay import TapToPay
from .transaction_reference import TransactionReference


class RefundPaymentMethodType(pydantic.BaseModel):
    """
    Object with one of the payment method type applicable for refund processing
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    ach: typing.Optional[Ach] = pydantic.Field(alias="ach", default=None)
    """
    Object for ACH (Automated Clearing House) payment method which occurs whenever someone instructs the ACH network to ?push? money from their account to someone else's. This is mostly used in USA.
    """
    card: typing.Optional[RefundCard] = pydantic.Field(alias="card", default=None)
    """
    Card payment instrument for refund
    """
    consumer_profile: typing.Optional[RefundConsumerProfile] = pydantic.Field(
        alias="consumerProfile", default=None
    )
    """
    Consumer Profile Payment method and attributes needed to process a refund transaction.
    """
    sepa: typing.Optional[Sepa] = pydantic.Field(alias="sepa", default=None)
    """
    Object for SEPA (Single Euro Payments Area) payment method is a regulatory initiative to facilitate cross border cashless payments across euro-using countries. SEPA allows people doing business across borders in euros to do so with the same ease as domestic transactions within the countries subject to SEPA.
    """
    tap_to_pay: typing.Optional[TapToPay] = pydantic.Field(
        alias="tapToPay", default=None
    )
    """
    Tap To Pay payment information
    """
    transaction_reference: typing.Optional[TransactionReference] = pydantic.Field(
        alias="transactionReference", default=None
    )
    """
    Object for refund transaction reference
    """
