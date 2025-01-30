import typing
import typing_extensions
import pydantic


class BillingVerification(typing_extensions.TypedDict):
    """
    Billing Verification results from payment network
    """

    consumer_first_name_verification_result: typing_extensions.NotRequired[
        typing_extensions.Literal["MATCH", "NO_MATCH", "PARTIAL_MATCH"]
    ]
    """
    Codifies the result of validation performed on customer name received in the authorization request. Null value indicates that Customer name check was not performed
    """

    consumer_full_name_verification_result: typing_extensions.NotRequired[
        typing_extensions.Literal["MATCH", "NO_MATCH", "PARTIAL_MATCH"]
    ]
    """
    Codifies the result of validation performed on customer name received in the authorization request. Null value indicates that Customer name check was not performed
    """

    consumer_last_name_verification_result: typing_extensions.NotRequired[
        typing_extensions.Literal["MATCH", "NO_MATCH", "PARTIAL_MATCH"]
    ]
    """
    Codifies the result of validation performed on customer name received in the authorization request. Null value indicates that Customer name check was not performed
    """

    consumer_middle_name_verification_result: typing_extensions.NotRequired[
        typing_extensions.Literal["MATCH", "NO_MATCH", "PARTIAL_MATCH"]
    ]
    """
    Codifies the result of validation performed on customer name received in the authorization request. Null value indicates that Customer name check was not performed
    """

    consumer_name_verification_result: typing_extensions.NotRequired[
        typing_extensions.Literal[
            "NAME_MATCH_ NOT_PERFORMED",
            "NAME_MATCH_ NOT_SUPPORTED",
            "NAME_MATCH_ PERFORMED",
        ]
    ]
    """
    Codifies the result of validation performed on customer name received in the authorization request. Null value indicates that Customer name check was not performed
    """


class _SerializerBillingVerification(pydantic.BaseModel):
    """
    Serializer for BillingVerification handling case conversions
    and file omissions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
        populate_by_name=True,
    )

    consumer_first_name_verification_result: typing.Optional[
        typing_extensions.Literal["MATCH", "NO_MATCH", "PARTIAL_MATCH"]
    ] = pydantic.Field(alias="consumerFirstNameVerificationResult", default=None)
    consumer_full_name_verification_result: typing.Optional[
        typing_extensions.Literal["MATCH", "NO_MATCH", "PARTIAL_MATCH"]
    ] = pydantic.Field(alias="consumerFullNameVerificationResult", default=None)
    consumer_last_name_verification_result: typing.Optional[
        typing_extensions.Literal["MATCH", "NO_MATCH", "PARTIAL_MATCH"]
    ] = pydantic.Field(alias="consumerLastNameVerificationResult", default=None)
    consumer_middle_name_verification_result: typing.Optional[
        typing_extensions.Literal["MATCH", "NO_MATCH", "PARTIAL_MATCH"]
    ] = pydantic.Field(alias="consumerMiddleNameVerificationResult", default=None)
    consumer_name_verification_result: typing.Optional[
        typing_extensions.Literal[
            "NAME_MATCH_ NOT_PERFORMED",
            "NAME_MATCH_ NOT_SUPPORTED",
            "NAME_MATCH_ PERFORMED",
        ]
    ] = pydantic.Field(alias="consumerNameVerificationResult", default=None)
