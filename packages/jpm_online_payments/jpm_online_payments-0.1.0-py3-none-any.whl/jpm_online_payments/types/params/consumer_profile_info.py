import typing
import typing_extensions
import pydantic


class ConsumerProfileInfo(typing_extensions.TypedDict):
    """
    Consumer profile Information if saved
    """

    consumer_profile_id: typing_extensions.NotRequired[str]
    """
    Identifies a unique occurrence of a consumer maintained in the firm as requested by merchant. Consumer profile contains information relevant to processing transactions such as name, address, account and payment methods information.
    """

    consumer_profile_request_type: typing_extensions.NotRequired[
        typing_extensions.Literal["CREATE"]
    ]
    """
    Codifies the nature of the ask for regarding consumer profile management
    """

    consumer_profile_response_code: typing_extensions.NotRequired[str]
    """
    Indicates whether profile creation was successful or resulted in an error.
    """

    consumer_profile_response_message: typing_extensions.NotRequired[str]
    """
    Confirms profile creation successful or describes reason for error.
    """

    external_consumer_profile_identifier: typing_extensions.NotRequired[str]
    """
    Identifies a unique occurrence of a consumer maintained by the merchant or a vendor. Consumer profile contains information relevant to processing transactions such as name, address, account and payment methods information.
    """

    legacy_consumer_profile_id: typing_extensions.NotRequired[str]
    """
    Identifies a unique occurrence of a consumer maintained in the firm as requested by merchant. Consumer profile contains information relevant to processing transactions such as name, address, account and payment methods information. Within this context, this is the Consumer Profile Identifier maintained in the firm's legacy system for the consumer.
    """

    payment_method_id: typing_extensions.NotRequired[str]
    """
    Identifies a unique occurrence of the type of payment accepted by a level of the hierarchy of the merchant acquiring account.
    """


class _SerializerConsumerProfileInfo(pydantic.BaseModel):
    """
    Serializer for ConsumerProfileInfo handling case conversions
    and file omissions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
        populate_by_name=True,
    )

    consumer_profile_id: typing.Optional[str] = pydantic.Field(
        alias="consumerProfileId", default=None
    )
    consumer_profile_request_type: typing.Optional[
        typing_extensions.Literal["CREATE"]
    ] = pydantic.Field(alias="consumerProfileRequestType", default=None)
    consumer_profile_response_code: typing.Optional[str] = pydantic.Field(
        alias="consumerProfileResponseCode", default=None
    )
    consumer_profile_response_message: typing.Optional[str] = pydantic.Field(
        alias="consumerProfileResponseMessage", default=None
    )
    external_consumer_profile_identifier: typing.Optional[str] = pydantic.Field(
        alias="externalConsumerProfileIdentifier", default=None
    )
    legacy_consumer_profile_id: typing.Optional[str] = pydantic.Field(
        alias="legacyConsumerProfileId", default=None
    )
    payment_method_id: typing.Optional[str] = pydantic.Field(
        alias="paymentMethodId", default=None
    )
