import typing
import pydantic

from .encrypted_payment_bundle import EncryptedPaymentBundle


class Applepay(pydantic.BaseModel):
    """
    Use is for encrypted bundles for web or Internet acceptance of digital device wallets such as Apple Pay
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    encrypted_payment_bundle: typing.Optional[EncryptedPaymentBundle] = pydantic.Field(
        alias="encryptedPaymentBundle", default=None
    )
    """
    Identifies encrypted bundle protocol version as defined by wallet.
    """
    lat_long: typing.Optional[str] = pydantic.Field(alias="latLong", default=None)
    """
    Identifies the latitude and longitude coordinates of the digital device when it is being provisioned. Information is expressed in the order of latitude then longitude with values rounded to the nearest whole digit.
    """
