import typing
import typing_extensions
import pydantic


class NetworkResponseAccountUpdater(typing_extensions.TypedDict):
    """
    Account update information as returned by the network
    """

    account_status: typing_extensions.NotRequired[
        typing_extensions.Literal["A", "C", "E", "Q"]
    ]
    """
    Identifies response code as defined by network. "A" PAN or PAN/Expiry change "E" Expiry change only "C" Closed account "Q" Contact cardholder
    """

    network_response_code: typing_extensions.NotRequired[str]
    """
    Network provided error or reason code
    """

    replacement_code: typing_extensions.NotRequired[bool]
    """
    Indicates if replacement of any information has occurred
    """


class _SerializerNetworkResponseAccountUpdater(pydantic.BaseModel):
    """
    Serializer for NetworkResponseAccountUpdater handling case conversions
    and file omissions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
        populate_by_name=True,
    )

    account_status: typing.Optional[typing_extensions.Literal["A", "C", "E", "Q"]] = (
        pydantic.Field(alias="accountStatus", default=None)
    )
    network_response_code: typing.Optional[str] = pydantic.Field(
        alias="networkResponseCode", default=None
    )
    replacement_code: typing.Optional[bool] = pydantic.Field(
        alias="replacementCode", default=None
    )
