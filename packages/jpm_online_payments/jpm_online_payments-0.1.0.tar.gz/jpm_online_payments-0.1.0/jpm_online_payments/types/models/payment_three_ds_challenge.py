import typing
import pydantic


class PaymentThreeDsChallenge(pydantic.BaseModel):
    """
    ThreeDS Challenge response from payment call.
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    authentication_status_reason_text: typing.Optional[str] = pydantic.Field(
        alias="authenticationStatusReasonText", default=None
    )
    """
    Long explanation of the Authentication Status
    """
    three_ds_acs_url: typing.Optional[str] = pydantic.Field(
        alias="threeDSAcsUrl", default=None
    )
    """
    Fully qualified URL of the ACS in case the authentication response message indicates that further Cardholder interaction is required to complete the authentication
    """
    update_timestamp: typing.Optional[str] = pydantic.Field(
        alias="updateTimestamp", default=None
    )
    """
    Designates the hour, minute, and second in a specific day when the record was last modified.
    """
