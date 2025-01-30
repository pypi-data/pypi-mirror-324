import typing
import pydantic

from .card_art import CardArt
from .wallet_card_data_card_meta_data import WalletCardDataCardMetaData


class WalletCardData(pydantic.BaseModel):
    """
    additional card information received from digital wallet provider.
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    card_art_list: typing.Optional[typing.List[CardArt]] = pydantic.Field(
        alias="cardArtList", default=None
    )
    """
    Card Art List
    """
    card_meta_data: typing.Optional[WalletCardDataCardMetaData] = pydantic.Field(
        alias="cardMetaData", default=None
    )
    """
    Card data, including its expiration date and suffix, for the card related to the merchant token.
    """
    wallet_merchant_token_reference_id: typing.Optional[str] = pydantic.Field(
        alias="walletMerchantTokenReferenceId", default=None
    )
    """
    Identifies uniquely a token provisioning request assigned by token service/vault and provided to Issuer and Wallet Provider. This can be used as a reference to the token number that is assigned for an account when provisioning completes. Example: DNITHE461927644624368716
    """
