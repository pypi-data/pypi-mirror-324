import typing
import typing_extensions
import pydantic

from .card_art import CardArt, _SerializerCardArt
from .wallet_card_data_card_meta_data import (
    WalletCardDataCardMetaData,
    _SerializerWalletCardDataCardMetaData,
)


class WalletCardData(typing_extensions.TypedDict):
    """
    additional card information received from digital wallet provider.
    """

    card_art_list: typing_extensions.NotRequired[typing.List[CardArt]]
    """
    Card Art List
    """

    card_meta_data: typing_extensions.NotRequired[WalletCardDataCardMetaData]
    """
    Card data, including its expiration date and suffix, for the card related to the merchant token.
    """

    wallet_merchant_token_reference_id: typing_extensions.NotRequired[str]
    """
    Identifies uniquely a token provisioning request assigned by token service/vault and provided to Issuer and Wallet Provider. This can be used as a reference to the token number that is assigned for an account when provisioning completes. Example: DNITHE461927644624368716
    """


class _SerializerWalletCardData(pydantic.BaseModel):
    """
    Serializer for WalletCardData handling case conversions
    and file omissions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
        populate_by_name=True,
    )

    card_art_list: typing.Optional[typing.List[_SerializerCardArt]] = pydantic.Field(
        alias="cardArtList", default=None
    )
    card_meta_data: typing.Optional[_SerializerWalletCardDataCardMetaData] = (
        pydantic.Field(alias="cardMetaData", default=None)
    )
    wallet_merchant_token_reference_id: typing.Optional[str] = pydantic.Field(
        alias="walletMerchantTokenReferenceId", default=None
    )
