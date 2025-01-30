import typing
import typing_extensions
import pydantic

from .ach import Ach, _SerializerAch
from .alipay import Alipay, _SerializerAlipay
from .applepay import Applepay, _SerializerApplepay
from .boleto import Boleto, _SerializerBoleto
from .card import Card, _SerializerCard
from .consumer_profile import ConsumerProfile, _SerializerConsumerProfile
from .giropay import Giropay, _SerializerGiropay
from .googlepay import Googlepay, _SerializerGooglepay
from .ideal import Ideal, _SerializerIdeal
from .paypal import Paypal, _SerializerPaypal
from .paze import Paze, _SerializerPaze
from .sepa import Sepa, _SerializerSepa
from .sofort import Sofort, _SerializerSofort
from .tap_to_pay import TapToPay, _SerializerTapToPay
from .trustly import Trustly, _SerializerTrustly
from .wechatpay import Wechatpay, _SerializerWechatpay


class PaymentMethodType(typing_extensions.TypedDict):
    """
    paymentType
    """

    ach: typing_extensions.NotRequired[Ach]
    """
    Object for ACH (Automated Clearing House) payment method which occurs whenever someone instructs the ACH network to ?push? money from their account to someone else's. This is mostly used in USA.
    """

    alipay: typing_extensions.NotRequired[Alipay]
    """
    Alipay payment method is a single-use payment method where customers are required to authenticate their payment.
    """

    applepay: typing_extensions.NotRequired[Applepay]
    """
    Use is for encrypted bundles for web or Internet acceptance of digital device wallets such as Apple Pay
    """

    boleto: typing_extensions.NotRequired[Boleto]
    """
    Boleto payment information
    """

    card: typing_extensions.NotRequired[Card]
    """
    Card payment instrument
    """

    consumer_profile: typing_extensions.NotRequired[ConsumerProfile]
    """
    Consumer Profile Payment method and attributes needed to process a transaction.
    """

    giropay: typing_extensions.NotRequired[Giropay]
    """
    Giropay is German based payment method that allows customers to complete transactions online using their online banking environment, with funds debited from their bank account.
    """

    googlepay: typing_extensions.NotRequired[Googlepay]
    """
    Use is for encrypted bundles for web or Internet acceptance of digital device wallets such as Google Pay
    """

    ideal: typing_extensions.NotRequired[Ideal]
    """
    Ideal is Netherland based payment method that allows customers to buy on the Internet using direct online transfers from their bank account.
    """

    paypal: typing_extensions.NotRequired[Paypal]
    """
    Paypal payment method
    """

    paze: typing_extensions.NotRequired[Paze]
    """
    Use is for encrypted bundles for web or Internet acceptance of digital device wallets PAZE
    """

    sepa: typing_extensions.NotRequired[Sepa]
    """
    Object for SEPA (Single Euro Payments Area) payment method is a regulatory initiative to facilitate cross border cashless payments across euro-using countries. SEPA allows people doing business across borders in euros to do so with the same ease as domestic transactions within the countries subject to SEPA.
    """

    sofort: typing_extensions.NotRequired[Sofort]
    """
    Sofort payment method is a single use, delayed notification payment method that requires customers to authenticate their payment
    """

    tap_to_pay: typing_extensions.NotRequired[TapToPay]
    """
    Tap To Pay payment information
    """

    trustly: typing_extensions.NotRequired[Trustly]
    """
    Trustly is an open banking payment method that allows customers to shop and pay from their online bank account, without the use of a card or app.
    """

    wechatpay: typing_extensions.NotRequired[Wechatpay]
    """
    Wechatpay payment method is linked to consumer bank accounts and/or payment network cards
    """


class _SerializerPaymentMethodType(pydantic.BaseModel):
    """
    Serializer for PaymentMethodType handling case conversions
    and file omissions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
        populate_by_name=True,
    )

    ach: typing.Optional[_SerializerAch] = pydantic.Field(alias="ach", default=None)
    alipay: typing.Optional[_SerializerAlipay] = pydantic.Field(
        alias="alipay", default=None
    )
    applepay: typing.Optional[_SerializerApplepay] = pydantic.Field(
        alias="applepay", default=None
    )
    boleto: typing.Optional[_SerializerBoleto] = pydantic.Field(
        alias="boleto", default=None
    )
    card: typing.Optional[_SerializerCard] = pydantic.Field(alias="card", default=None)
    consumer_profile: typing.Optional[_SerializerConsumerProfile] = pydantic.Field(
        alias="consumerProfile", default=None
    )
    giropay: typing.Optional[_SerializerGiropay] = pydantic.Field(
        alias="giropay", default=None
    )
    googlepay: typing.Optional[_SerializerGooglepay] = pydantic.Field(
        alias="googlepay", default=None
    )
    ideal: typing.Optional[_SerializerIdeal] = pydantic.Field(
        alias="ideal", default=None
    )
    paypal: typing.Optional[_SerializerPaypal] = pydantic.Field(
        alias="paypal", default=None
    )
    paze: typing.Optional[_SerializerPaze] = pydantic.Field(alias="paze", default=None)
    sepa: typing.Optional[_SerializerSepa] = pydantic.Field(alias="sepa", default=None)
    sofort: typing.Optional[_SerializerSofort] = pydantic.Field(
        alias="sofort", default=None
    )
    tap_to_pay: typing.Optional[_SerializerTapToPay] = pydantic.Field(
        alias="tapToPay", default=None
    )
    trustly: typing.Optional[_SerializerTrustly] = pydantic.Field(
        alias="trustly", default=None
    )
    wechatpay: typing.Optional[_SerializerWechatpay] = pydantic.Field(
        alias="wechatpay", default=None
    )
