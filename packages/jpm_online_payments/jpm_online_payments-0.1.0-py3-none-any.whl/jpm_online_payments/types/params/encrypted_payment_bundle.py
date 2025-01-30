import typing
import typing_extensions
import pydantic

from .encrypted_payment_header import (
    EncryptedPaymentHeader,
    _SerializerEncryptedPaymentHeader,
)


class EncryptedPaymentBundle(typing_extensions.TypedDict):
    """
    Identifies encrypted bundle protocol version as defined by wallet.
    """

    encrypted_payload: typing_extensions.NotRequired[str]
    """
    Encrypted message details have been rendered unreadable by general means through the application of a given set of instructions and a key.
    """

    encrypted_payment_header: typing_extensions.NotRequired[EncryptedPaymentHeader]
    """
    header information for Encrypted Data from ApplePay, GooglePay or Paze.
    """

    protocol_version: typing_extensions.NotRequired[str]
    """
    Identifies encrypted bundle protocol version as defined by wallet.
    """

    signature: typing_extensions.NotRequired[str]
    """
    This is the virtual signature data of the payment and header data. The signature information let the receiver know that the data is indeed sent by the sender. The signature is created using sender's key pair.
    """


class _SerializerEncryptedPaymentBundle(pydantic.BaseModel):
    """
    Serializer for EncryptedPaymentBundle handling case conversions
    and file omissions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
        populate_by_name=True,
    )

    encrypted_payload: typing.Optional[str] = pydantic.Field(
        alias="encryptedPayload", default=None
    )
    encrypted_payment_header: typing.Optional[_SerializerEncryptedPaymentHeader] = (
        pydantic.Field(alias="encryptedPaymentHeader", default=None)
    )
    protocol_version: typing.Optional[str] = pydantic.Field(
        alias="protocolVersion", default=None
    )
    signature: typing.Optional[str] = pydantic.Field(alias="signature", default=None)
