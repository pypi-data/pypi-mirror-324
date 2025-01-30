import typing
import typing_extensions
import pydantic


class ThreeDsRequestorAuthenticationInfo(pydantic.BaseModel):
    """
    Information about how the 3DS Requestor authenticated the cardholder before or during the transaction.
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    authentication_purpose: typing_extensions.Literal[
        "ADD_CARD",
        "BILLING_AGREEMENT",
        "CARDHOLDER_VERIFICATION",
        "INSTALLMENT_TRANSACTION",
        "MAINTAIN_CARD",
        "PAYMENT_TRANSACTION",
        "RECURRING_TRANSACTION",
    ] = pydantic.Field(
        alias="authenticationPurpose",
    )
    """
    Indicates the type of Authentication request.threeDSRequestorPriorAuthenticationInfo
    """
    requestor_authentication_method: typing.Optional[
        typing_extensions.Literal[
            "FEDERATED_ID", "FIDO", "ISSUER_CRED", "NONE", "REQUESTOR_CRED"
        ]
    ] = pydantic.Field(alias="requestorAuthenticationMethod", default=None)
    """
    Information about how the 3DS Requestor authenticated the cardholder before or during the transaction.
    """
    three_ds_authentication_data: typing.Optional[str] = pydantic.Field(
        alias="threeDSAuthenticationData", default=None
    )
    """
    Data that documents and supports a specific authentication process.
    """
    three_ds_authentication_timestamp: typing.Optional[str] = pydantic.Field(
        alias="threeDSAuthenticationTimestamp", default=None
    )
    """
    Designates the hour, minute and second  of the cardholder authentication
    """
    three_ds_challenge_type: typing.Optional[
        typing_extensions.Literal[
            "CHALLENGE_MANDATE",
            "CHALLENGE_REQUESTED",
            "NO_CHALLENGE",
            "NO_CHALLENGE_DA",
            "NO_CHALLENGE_DATA",
            "NO_CHALLENGE_TRA",
            "NO_CHALLENGE_TRUSTED",
            "NO_PREFERENCE",
        ]
    ] = pydantic.Field(alias="threeDSChallengeType", default=None)
    """
    Indicates whether a challenge is requested for this transaction.
    """
