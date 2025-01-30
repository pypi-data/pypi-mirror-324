import typing
import typing_extensions
import pydantic


class WalletCardDataCardMetaData(typing_extensions.TypedDict, total=False):
    """
    Card data, including its expiration date and suffix, for the card related to the merchant token.
    """


class _SerializerWalletCardDataCardMetaData(pydantic.BaseModel):
    """
    Serializer for WalletCardDataCardMetaData handling case conversions
    and file omissions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
        populate_by_name=True,
        extra="allow",
    )
    __pydantic_extra__: typing.Dict[str, str]
