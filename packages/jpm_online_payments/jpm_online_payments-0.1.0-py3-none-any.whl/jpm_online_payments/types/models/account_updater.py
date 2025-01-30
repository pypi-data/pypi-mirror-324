import typing
import typing_extensions
import pydantic

from .pan_expiry import PanExpiry


class AccountUpdater(pydantic.BaseModel):
    """
    Contains response information related to account updater request
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    account_number: typing.Optional[str] = pydantic.Field(
        alias="accountNumber", default=None
    )
    """
    Updated Account Number if available from Account Updater service.
    """
    account_updater_reason_code: typing.Optional[str] = pydantic.Field(
        alias="accountUpdaterReasonCode", default=None
    )
    """
    Indicates whether Account Updater service was successfully evoked or if there was an error. "SUCCESS" or "ERROR."
    """
    account_updater_reason_message: typing.Optional[str] = pydantic.Field(
        alias="accountUpdaterReasonMessage", default=None
    )
    """
    Long description of account updater results. e.g. "Account Update provided for account expiry "
    """
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
    """
    Result of account updater request.
    """
    new_account_expiry: typing.Optional[PanExpiry] = pydantic.Field(
        alias="newAccountExpiry", default=None
    )
    """
    Contains expiry for masked PAN if received from network
    """
    request_account_updater: typing.Optional[bool] = pydantic.Field(
        alias="requestAccountUpdater", default=None
    )
    """
    Indicates whether Visa Real-Time Account Updater service should be utilized. Merchants must be enrolled in service and payments must be recurring or stored. If enrolled merchant does not pass field and transaction qualifies, default is "TRUE."
    """
