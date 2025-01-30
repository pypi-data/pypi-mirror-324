import typing
import typing_extensions
import pydantic


class ThreeDsRequestorPriorAuthenticationInfo(typing_extensions.TypedDict):
    """
    Contains information about how the 3DS Requestor authenticated the cardholder as part of a previous 3DS transaction.
    """

    authentication_method: typing_extensions.NotRequired[
        typing_extensions.Literal["AVS_VERIFIED", "CHALLENGED", "FRICTIONLESS", "OTHER"]
    ]
    """
    Information about how the 3DS Requestor previously  authenticated the cardholder.
    """

    authentication_timestamp: typing_extensions.NotRequired[str]
    """
    Designates the hour, minute and second of the prior authentication.
    """

    prior_acs_transaction_id: typing_extensions.NotRequired[str]
    """
    ACS Transaction ID for a prior authenticated transaction
    """


class _SerializerThreeDsRequestorPriorAuthenticationInfo(pydantic.BaseModel):
    """
    Serializer for ThreeDsRequestorPriorAuthenticationInfo handling case conversions
    and file omissions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
        populate_by_name=True,
    )

    authentication_method: typing.Optional[
        typing_extensions.Literal["AVS_VERIFIED", "CHALLENGED", "FRICTIONLESS", "OTHER"]
    ] = pydantic.Field(alias="authenticationMethod", default=None)
    authentication_timestamp: typing.Optional[str] = pydantic.Field(
        alias="authenticationTimestamp", default=None
    )
    prior_acs_transaction_id: typing.Optional[str] = pydantic.Field(
        alias="priorAcsTransactionId", default=None
    )
