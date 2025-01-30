import typing
import typing_extensions
import pydantic

from .encrypted_payment_bundle import (
    EncryptedPaymentBundle,
    _SerializerEncryptedPaymentBundle,
)


class Applepay(typing_extensions.TypedDict):
    """
    Use is for encrypted bundles for web or Internet acceptance of digital device wallets such as Apple Pay
    """

    encrypted_payment_bundle: typing_extensions.NotRequired[EncryptedPaymentBundle]
    """
    Identifies encrypted bundle protocol version as defined by wallet.
    """

    lat_long: typing_extensions.NotRequired[str]
    """
    Identifies the latitude and longitude coordinates of the digital device when it is being provisioned. Information is expressed in the order of latitude then longitude with values rounded to the nearest whole digit.
    """


class _SerializerApplepay(pydantic.BaseModel):
    """
    Serializer for Applepay handling case conversions
    and file omissions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
        populate_by_name=True,
    )

    encrypted_payment_bundle: typing.Optional[_SerializerEncryptedPaymentBundle] = (
        pydantic.Field(alias="encryptedPaymentBundle", default=None)
    )
    lat_long: typing.Optional[str] = pydantic.Field(alias="latLong", default=None)
