import typing
import typing_extensions
import pydantic


class ThreeDomainSecureExemption(pydantic.BaseModel):
    """
    Three Domain Secure Closure
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    authentication_exemption_reason: typing.Optional[
        typing_extensions.Literal[
            "LOW_VALUE_PAYMENT",
            "MERCHANT_INITIATED_TRANSACTION",
            "NOT_ENTITLED",
            "NOT_EXEMPTED",
            "ONE_LEG_OUT",
            "RECURRING_PAYMENT",
            "TRANSACTION_RISK_ANALYSIS",
        ]
    ] = pydantic.Field(alias="authenticationExemptionReason", default=None)
    """
    EEA/UK Supported SCA exemptions
    """
    authentication_status_reason_text: typing.Optional[str] = pydantic.Field(
        alias="authenticationStatusReasonText", default=None
    )
    """
    Long explanation of the Authentication Status
    """
    update_timestamp: typing.Optional[str] = pydantic.Field(
        alias="updateTimestamp", default=None
    )
    """
    Designates the hour, minute, and second in a specific day when the record was last modified.
    """
