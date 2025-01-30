import typing
import pydantic

from .ach import Ach
from .alipay import Alipay
from .applepay import Applepay
from .boleto import Boleto
from .card import Card
from .consumer_profile import ConsumerProfile
from .giropay import Giropay
from .googlepay import Googlepay
from .ideal import Ideal
from .paypal import Paypal
from .paze import Paze
from .sepa import Sepa
from .sofort import Sofort
from .tap_to_pay import TapToPay
from .trustly import Trustly
from .wechatpay import Wechatpay


class PaymentMethodType(pydantic.BaseModel):
    """
    paymentType
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    ach: typing.Optional[Ach] = pydantic.Field(alias="ach", default=None)
    """
    Object for ACH (Automated Clearing House) payment method which occurs whenever someone instructs the ACH network to ?push? money from their account to someone else's. This is mostly used in USA.
    """
    alipay: typing.Optional[Alipay] = pydantic.Field(alias="alipay", default=None)
    """
    Alipay payment method is a single-use payment method where customers are required to authenticate their payment.
    """
    applepay: typing.Optional[Applepay] = pydantic.Field(alias="applepay", default=None)
    """
    Use is for encrypted bundles for web or Internet acceptance of digital device wallets such as Apple Pay
    """
    boleto: typing.Optional[Boleto] = pydantic.Field(alias="boleto", default=None)
    """
    Boleto payment information
    """
    card: typing.Optional[Card] = pydantic.Field(alias="card", default=None)
    """
    Card payment instrument
    """
    consumer_profile: typing.Optional[ConsumerProfile] = pydantic.Field(
        alias="consumerProfile", default=None
    )
    """
    Consumer Profile Payment method and attributes needed to process a transaction.
    """
    giropay: typing.Optional[Giropay] = pydantic.Field(alias="giropay", default=None)
    """
    Giropay is German based payment method that allows customers to complete transactions online using their online banking environment, with funds debited from their bank account.
    """
    googlepay: typing.Optional[Googlepay] = pydantic.Field(
        alias="googlepay", default=None
    )
    """
    Use is for encrypted bundles for web or Internet acceptance of digital device wallets such as Google Pay
    """
    ideal: typing.Optional[Ideal] = pydantic.Field(alias="ideal", default=None)
    """
    Ideal is Netherland based payment method that allows customers to buy on the Internet using direct online transfers from their bank account.
    """
    paypal: typing.Optional[Paypal] = pydantic.Field(alias="paypal", default=None)
    """
    Paypal payment method
    """
    paze: typing.Optional[Paze] = pydantic.Field(alias="paze", default=None)
    """
    Use is for encrypted bundles for web or Internet acceptance of digital device wallets PAZE
    """
    sepa: typing.Optional[Sepa] = pydantic.Field(alias="sepa", default=None)
    """
    Object for SEPA (Single Euro Payments Area) payment method is a regulatory initiative to facilitate cross border cashless payments across euro-using countries. SEPA allows people doing business across borders in euros to do so with the same ease as domestic transactions within the countries subject to SEPA.
    """
    sofort: typing.Optional[Sofort] = pydantic.Field(alias="sofort", default=None)
    """
    Sofort payment method is a single use, delayed notification payment method that requires customers to authenticate their payment
    """
    tap_to_pay: typing.Optional[TapToPay] = pydantic.Field(
        alias="tapToPay", default=None
    )
    """
    Tap To Pay payment information
    """
    trustly: typing.Optional[Trustly] = pydantic.Field(alias="trustly", default=None)
    """
    Trustly is an open banking payment method that allows customers to shop and pay from their online bank account, without the use of a card or app.
    """
    wechatpay: typing.Optional[Wechatpay] = pydantic.Field(
        alias="wechatpay", default=None
    )
    """
    Wechatpay payment method is linked to consumer bank accounts and/or payment network cards
    """
