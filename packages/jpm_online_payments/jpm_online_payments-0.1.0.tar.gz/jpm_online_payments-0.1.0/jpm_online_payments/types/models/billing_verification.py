import typing
import typing_extensions
import pydantic


class BillingVerification(pydantic.BaseModel):
    """
    Billing Verification results from payment network
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    consumer_first_name_verification_result: typing.Optional[
        typing_extensions.Literal["MATCH", "NO_MATCH", "PARTIAL_MATCH"]
    ] = pydantic.Field(alias="consumerFirstNameVerificationResult", default=None)
    """
    Codifies the result of validation performed on customer name received in the authorization request. Null value indicates that Customer name check was not performed
    """
    consumer_full_name_verification_result: typing.Optional[
        typing_extensions.Literal["MATCH", "NO_MATCH", "PARTIAL_MATCH"]
    ] = pydantic.Field(alias="consumerFullNameVerificationResult", default=None)
    """
    Codifies the result of validation performed on customer name received in the authorization request. Null value indicates that Customer name check was not performed
    """
    consumer_last_name_verification_result: typing.Optional[
        typing_extensions.Literal["MATCH", "NO_MATCH", "PARTIAL_MATCH"]
    ] = pydantic.Field(alias="consumerLastNameVerificationResult", default=None)
    """
    Codifies the result of validation performed on customer name received in the authorization request. Null value indicates that Customer name check was not performed
    """
    consumer_middle_name_verification_result: typing.Optional[
        typing_extensions.Literal["MATCH", "NO_MATCH", "PARTIAL_MATCH"]
    ] = pydantic.Field(alias="consumerMiddleNameVerificationResult", default=None)
    """
    Codifies the result of validation performed on customer name received in the authorization request. Null value indicates that Customer name check was not performed
    """
    consumer_name_verification_result: typing.Optional[
        typing_extensions.Literal[
            "NAME_MATCH_ NOT_PERFORMED",
            "NAME_MATCH_ NOT_SUPPORTED",
            "NAME_MATCH_ PERFORMED",
        ]
    ] = pydantic.Field(alias="consumerNameVerificationResult", default=None)
    """
    Codifies the result of validation performed on customer name received in the authorization request. Null value indicates that Customer name check was not performed
    """
