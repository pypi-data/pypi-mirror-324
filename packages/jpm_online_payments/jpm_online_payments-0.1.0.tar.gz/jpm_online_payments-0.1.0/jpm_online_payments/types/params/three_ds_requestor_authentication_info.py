import typing
import typing_extensions
import pydantic


class ThreeDsRequestorAuthenticationInfo(typing_extensions.TypedDict):
    """
    Information about how the 3DS Requestor authenticated the cardholder before or during the transaction.
    """

    authentication_purpose: typing_extensions.Required[
        typing_extensions.Literal[
            "ADD_CARD",
            "BILLING_AGREEMENT",
            "CARDHOLDER_VERIFICATION",
            "INSTALLMENT_TRANSACTION",
            "MAINTAIN_CARD",
            "PAYMENT_TRANSACTION",
            "RECURRING_TRANSACTION",
        ]
    ]
    """
    Indicates the type of Authentication request.threeDSRequestorPriorAuthenticationInfo
    """

    requestor_authentication_method: typing_extensions.NotRequired[
        typing_extensions.Literal[
            "FEDERATED_ID", "FIDO", "ISSUER_CRED", "NONE", "REQUESTOR_CRED"
        ]
    ]
    """
    Information about how the 3DS Requestor authenticated the cardholder before or during the transaction.
    """

    three_ds_authentication_data: typing_extensions.NotRequired[str]
    """
    Data that documents and supports a specific authentication process.
    """

    three_ds_authentication_timestamp: typing_extensions.NotRequired[str]
    """
    Designates the hour, minute and second  of the cardholder authentication
    """

    three_ds_challenge_type: typing_extensions.NotRequired[
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
    ]
    """
    Indicates whether a challenge is requested for this transaction.
    """


class _SerializerThreeDsRequestorAuthenticationInfo(pydantic.BaseModel):
    """
    Serializer for ThreeDsRequestorAuthenticationInfo handling case conversions
    and file omissions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
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
    requestor_authentication_method: typing.Optional[
        typing_extensions.Literal[
            "FEDERATED_ID", "FIDO", "ISSUER_CRED", "NONE", "REQUESTOR_CRED"
        ]
    ] = pydantic.Field(alias="requestorAuthenticationMethod", default=None)
    three_ds_authentication_data: typing.Optional[str] = pydantic.Field(
        alias="threeDSAuthenticationData", default=None
    )
    three_ds_authentication_timestamp: typing.Optional[str] = pydantic.Field(
        alias="threeDSAuthenticationTimestamp", default=None
    )
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
