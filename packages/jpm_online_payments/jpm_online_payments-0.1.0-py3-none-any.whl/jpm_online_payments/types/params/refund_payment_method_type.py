import typing
import typing_extensions
import pydantic

from .ach import Ach, _SerializerAch
from .refund_card import RefundCard, _SerializerRefundCard
from .refund_consumer_profile import (
    RefundConsumerProfile,
    _SerializerRefundConsumerProfile,
)
from .sepa import Sepa, _SerializerSepa
from .tap_to_pay import TapToPay, _SerializerTapToPay
from .transaction_reference import TransactionReference, _SerializerTransactionReference


class RefundPaymentMethodType(typing_extensions.TypedDict):
    """
    Object with one of the payment method type applicable for refund processing
    """

    ach: typing_extensions.NotRequired[Ach]
    """
    Object for ACH (Automated Clearing House) payment method which occurs whenever someone instructs the ACH network to ?push? money from their account to someone else's. This is mostly used in USA.
    """

    card: typing_extensions.NotRequired[RefundCard]
    """
    Card payment instrument for refund
    """

    consumer_profile: typing_extensions.NotRequired[RefundConsumerProfile]
    """
    Consumer Profile Payment method and attributes needed to process a refund transaction.
    """

    sepa: typing_extensions.NotRequired[Sepa]
    """
    Object for SEPA (Single Euro Payments Area) payment method is a regulatory initiative to facilitate cross border cashless payments across euro-using countries. SEPA allows people doing business across borders in euros to do so with the same ease as domestic transactions within the countries subject to SEPA.
    """

    tap_to_pay: typing_extensions.NotRequired[TapToPay]
    """
    Tap To Pay payment information
    """

    transaction_reference: typing_extensions.NotRequired[TransactionReference]
    """
    Object for refund transaction reference
    """


class _SerializerRefundPaymentMethodType(pydantic.BaseModel):
    """
    Serializer for RefundPaymentMethodType handling case conversions
    and file omissions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
        populate_by_name=True,
    )

    ach: typing.Optional[_SerializerAch] = pydantic.Field(alias="ach", default=None)
    card: typing.Optional[_SerializerRefundCard] = pydantic.Field(
        alias="card", default=None
    )
    consumer_profile: typing.Optional[_SerializerRefundConsumerProfile] = (
        pydantic.Field(alias="consumerProfile", default=None)
    )
    sepa: typing.Optional[_SerializerSepa] = pydantic.Field(alias="sepa", default=None)
    tap_to_pay: typing.Optional[_SerializerTapToPay] = pydantic.Field(
        alias="tapToPay", default=None
    )
    transaction_reference: typing.Optional[_SerializerTransactionReference] = (
        pydantic.Field(alias="transactionReference", default=None)
    )
