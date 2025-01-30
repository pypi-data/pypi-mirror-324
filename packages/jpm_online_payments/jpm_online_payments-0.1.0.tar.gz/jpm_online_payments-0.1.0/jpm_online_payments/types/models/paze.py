import typing
import pydantic

from .encrypted_payment_bundle import EncryptedPaymentBundle


class Paze(pydantic.BaseModel):
    """
    Use is for encrypted bundles for web or Internet acceptance of digital device wallets PAZE
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
