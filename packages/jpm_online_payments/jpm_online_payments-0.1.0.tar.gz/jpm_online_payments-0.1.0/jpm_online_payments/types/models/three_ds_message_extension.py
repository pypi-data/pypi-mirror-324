import typing
import pydantic


class ThreeDsMessageExtension(pydantic.BaseModel):
    """
    Contains Data necessary to support requirements not otherwise defined in the 3D Secure message are carried in a Message Extension. This field is limited to 81.920 characters and it is used in the Authentication Request.
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    message_extension_criticality: typing.Optional[bool] = pydantic.Field(
        alias="messageExtensionCriticality", default=None
    )
    """
    Indicate if the additional message is critical for the cardholder authentication process by the vendor. The additional message necessary to support requirements not otherwise defined in the 3D Secure message.
    """
    message_extension_data: typing.Optional[str] = pydantic.Field(
        alias="messageExtensionData", default=None
    )
    """
    The additional textual data carried in the extension to support requirements not otherwise defined in the 3D Secure message.
    """
    message_extension_id: typing.Optional[str] = pydantic.Field(
        alias="messageExtensionId", default=None
    )
    """
    A unique identifier for the additional message necessary to support requirements not otherwise defined in the 3D Secure message.
    """
    message_extension_name: typing.Optional[str] = pydantic.Field(
        alias="messageExtensionName", default=None
    )
    """
    The label for additional message necessary to support requirements not otherwise defined in the 3D Secure message.
    """
