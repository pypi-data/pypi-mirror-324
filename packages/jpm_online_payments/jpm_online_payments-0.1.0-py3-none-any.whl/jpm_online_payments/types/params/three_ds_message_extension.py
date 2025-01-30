import typing
import typing_extensions
import pydantic


class ThreeDsMessageExtension(typing_extensions.TypedDict):
    """
    Contains Data necessary to support requirements not otherwise defined in the 3D Secure message are carried in a Message Extension. This field is limited to 81.920 characters and it is used in the Authentication Request.
    """

    message_extension_criticality: typing_extensions.NotRequired[bool]
    """
    Indicate if the additional message is critical for the cardholder authentication process by the vendor. The additional message necessary to support requirements not otherwise defined in the 3D Secure message.
    """

    message_extension_data: typing_extensions.NotRequired[str]
    """
    The additional textual data carried in the extension to support requirements not otherwise defined in the 3D Secure message.
    """

    message_extension_id: typing_extensions.NotRequired[str]
    """
    A unique identifier for the additional message necessary to support requirements not otherwise defined in the 3D Secure message.
    """

    message_extension_name: typing_extensions.NotRequired[str]
    """
    The label for additional message necessary to support requirements not otherwise defined in the 3D Secure message.
    """


class _SerializerThreeDsMessageExtension(pydantic.BaseModel):
    """
    Serializer for ThreeDsMessageExtension handling case conversions
    and file omissions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
        populate_by_name=True,
    )

    message_extension_criticality: typing.Optional[bool] = pydantic.Field(
        alias="messageExtensionCriticality", default=None
    )
    message_extension_data: typing.Optional[str] = pydantic.Field(
        alias="messageExtensionData", default=None
    )
    message_extension_id: typing.Optional[str] = pydantic.Field(
        alias="messageExtensionId", default=None
    )
    message_extension_name: typing.Optional[str] = pydantic.Field(
        alias="messageExtensionName", default=None
    )
