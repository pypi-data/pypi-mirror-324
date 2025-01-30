import typing
import typing_extensions
import pydantic

from .encrypted_payment_bundle import (
    EncryptedPaymentBundle,
    _SerializerEncryptedPaymentBundle,
)


class Paze(typing_extensions.TypedDict):
    """
    Use is for encrypted bundles for web or Internet acceptance of digital device wallets PAZE
    """

    encrypted_payment_bundle: typing_extensions.NotRequired[EncryptedPaymentBundle]
    """
    Identifies encrypted bundle protocol version as defined by wallet.
    """


class _SerializerPaze(pydantic.BaseModel):
    """
    Serializer for Paze handling case conversions
    and file omissions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
        populate_by_name=True,
    )

    encrypted_payment_bundle: typing.Optional[_SerializerEncryptedPaymentBundle] = (
        pydantic.Field(alias="encryptedPaymentBundle", default=None)
    )
