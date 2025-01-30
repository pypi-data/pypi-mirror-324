import typing
import typing_extensions
import pydantic


class NetworkResponseAccountUpdater(pydantic.BaseModel):
    """
    Account update information as returned by the network
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    account_status: typing.Optional[typing_extensions.Literal["A", "C", "E", "Q"]] = (
        pydantic.Field(alias="accountStatus", default=None)
    )
    """
    Identifies response code as defined by network. "A" PAN or PAN/Expiry change "E" Expiry change only "C" Closed account "Q" Contact cardholder
    """
    network_response_code: typing.Optional[str] = pydantic.Field(
        alias="networkResponseCode", default=None
    )
    """
    Network provided error or reason code
    """
    replacement_code: typing.Optional[bool] = pydantic.Field(
        alias="replacementCode", default=None
    )
    """
    Indicates if replacement of any information has occurred
    """
