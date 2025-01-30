import typing
import pydantic

from .encrypted_payment_header import EncryptedPaymentHeader


class EncryptedPaymentBundle(pydantic.BaseModel):
    """
    Identifies encrypted bundle protocol version as defined by wallet.
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    encrypted_payload: typing.Optional[str] = pydantic.Field(
        alias="encryptedPayload", default=None
    )
    """
    Encrypted message details have been rendered unreadable by general means through the application of a given set of instructions and a key.
    """
    encrypted_payment_header: typing.Optional[EncryptedPaymentHeader] = pydantic.Field(
        alias="encryptedPaymentHeader", default=None
    )
    """
    header information for Encrypted Data from ApplePay, GooglePay or Paze.
    """
    protocol_version: typing.Optional[str] = pydantic.Field(
        alias="protocolVersion", default=None
    )
    """
    Identifies encrypted bundle protocol version as defined by wallet.
    """
    signature: typing.Optional[str] = pydantic.Field(alias="signature", default=None)
    """
    This is the virtual signature data of the payment and header data. The signature information let the receiver know that the data is indeed sent by the sender. The signature is created using sender's key pair.
    """
