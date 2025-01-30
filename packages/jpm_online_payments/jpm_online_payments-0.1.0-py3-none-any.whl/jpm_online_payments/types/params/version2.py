import typing
import typing_extensions
import pydantic


class Version2(typing_extensions.TypedDict):
    """
    Contains information about payer authentication using 3-D Secure authentication version 2
    """

    three_ds_transaction_status: typing_extensions.NotRequired[
        typing_extensions.Literal["A", "C", "D", "I", "N", "R", "U", "Y"]
    ]
    """
    Indicates whether a transaction qualifies as an authenticated transaction. The accepted values are: Y -> Authentication / Account verification successful N -> Not authenticated / Account not verified; Transaction denied U -> Authentication / Account verification could not be performed; technical or other problem C -> In order to complete the authentication, a challenge is required R -> Authentication / Account verification Rejected. Issuer is rejecting authentication/verification and request that authorization not be attempted A -> Attempts processing performed; Not authenticated / verified, but a proof of attempt authentication / verification is provided The following values are also accepted if the 3DS Server has initiated authentication with EMV 3DS 2.2.0 version or greater: D -> In order to complete the authentication, a challenge is required. Decoupled Authentication confirmed. I -> Informational Only; 3DS Requestor challenge preference acknowledged
    """

    three_ds_transaction_status_reason_code: typing_extensions.NotRequired[str]
    """
    Contains code indicating the reason for the transaction status in threeDSTransactionStatus.
    """


class _SerializerVersion2(pydantic.BaseModel):
    """
    Serializer for Version2 handling case conversions
    and file omissions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
        populate_by_name=True,
    )

    three_ds_transaction_status: typing.Optional[
        typing_extensions.Literal["A", "C", "D", "I", "N", "R", "U", "Y"]
    ] = pydantic.Field(alias="threeDSTransactionStatus", default=None)
    three_ds_transaction_status_reason_code: typing.Optional[str] = pydantic.Field(
        alias="threeDSTransactionStatusReasonCode", default=None
    )
