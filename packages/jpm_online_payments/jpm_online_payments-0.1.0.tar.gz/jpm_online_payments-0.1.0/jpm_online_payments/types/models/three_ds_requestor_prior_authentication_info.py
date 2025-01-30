import typing
import typing_extensions
import pydantic


class ThreeDsRequestorPriorAuthenticationInfo(pydantic.BaseModel):
    """
    Contains information about how the 3DS Requestor authenticated the cardholder as part of a previous 3DS transaction.
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    authentication_method: typing.Optional[
        typing_extensions.Literal["AVS_VERIFIED", "CHALLENGED", "FRICTIONLESS", "OTHER"]
    ] = pydantic.Field(alias="authenticationMethod", default=None)
    """
    Information about how the 3DS Requestor previously  authenticated the cardholder.
    """
    authentication_timestamp: typing.Optional[str] = pydantic.Field(
        alias="authenticationTimestamp", default=None
    )
    """
    Designates the hour, minute and second of the prior authentication.
    """
    prior_acs_transaction_id: typing.Optional[str] = pydantic.Field(
        alias="priorAcsTransactionId", default=None
    )
    """
    ACS Transaction ID for a prior authenticated transaction
    """
