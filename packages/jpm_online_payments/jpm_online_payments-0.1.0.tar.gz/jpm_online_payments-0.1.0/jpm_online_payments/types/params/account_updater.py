import typing
import typing_extensions
import pydantic

from .pan_expiry import PanExpiry, _SerializerPanExpiry


class AccountUpdater(typing_extensions.TypedDict):
    """
    Contains response information related to account updater request
    """

    account_number: typing_extensions.NotRequired[str]
    """
    Updated Account Number if available from Account Updater service.
    """

    account_updater_reason_code: typing_extensions.NotRequired[str]
    """
    Indicates whether Account Updater service was successfully evoked or if there was an error. "SUCCESS" or "ERROR."
    """

    account_updater_reason_message: typing_extensions.NotRequired[str]
    """
    Long description of account updater results. e.g. "Account Update provided for account expiry "
    """

    account_updater_response: typing_extensions.NotRequired[
        typing_extensions.Literal[
            "CARDHOLDER_OPT_OUT",
            "CLOSED_ACCOUNT",
            "CONTACT_CARDHOLDER",
            "ISSUER_NOT_PARTICIPATING",
            "MATCH_NO_UPDATE",
            "NEW_ACCOUNT",
            "NEW_ACCOUNT_AND_EXPIRY",
            "NEW_EXPIRY",
            "NO_MATCH_NON_PARTICIPATING_BIN",
            "NO_MATCH_PARTICIPATING_BIN",
            "PORTFOLIO_CONVERSION",
            "PROVIDED_EXPIRY_NEWER",
        ]
    ]
    """
    Result of account updater request.
    """

    new_account_expiry: typing_extensions.NotRequired[PanExpiry]
    """
    Contains expiry for masked PAN if received from network
    """

    request_account_updater: typing_extensions.NotRequired[bool]
    """
    Indicates whether Visa Real-Time Account Updater service should be utilized. Merchants must be enrolled in service and payments must be recurring or stored. If enrolled merchant does not pass field and transaction qualifies, default is "TRUE."
    """


class _SerializerAccountUpdater(pydantic.BaseModel):
    """
    Serializer for AccountUpdater handling case conversions
    and file omissions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
        populate_by_name=True,
    )

    account_number: typing.Optional[str] = pydantic.Field(
        alias="accountNumber", default=None
    )
    account_updater_reason_code: typing.Optional[str] = pydantic.Field(
        alias="accountUpdaterReasonCode", default=None
    )
    account_updater_reason_message: typing.Optional[str] = pydantic.Field(
        alias="accountUpdaterReasonMessage", default=None
    )
    account_updater_response: typing.Optional[
        typing_extensions.Literal[
            "CARDHOLDER_OPT_OUT",
            "CLOSED_ACCOUNT",
            "CONTACT_CARDHOLDER",
            "ISSUER_NOT_PARTICIPATING",
            "MATCH_NO_UPDATE",
            "NEW_ACCOUNT",
            "NEW_ACCOUNT_AND_EXPIRY",
            "NEW_EXPIRY",
            "NO_MATCH_NON_PARTICIPATING_BIN",
            "NO_MATCH_PARTICIPATING_BIN",
            "PORTFOLIO_CONVERSION",
            "PROVIDED_EXPIRY_NEWER",
        ]
    ] = pydantic.Field(alias="accountUpdaterResponse", default=None)
    new_account_expiry: typing.Optional[_SerializerPanExpiry] = pydantic.Field(
        alias="newAccountExpiry", default=None
    )
    request_account_updater: typing.Optional[bool] = pydantic.Field(
        alias="requestAccountUpdater", default=None
    )
