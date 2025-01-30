import typing
import typing_extensions
import pydantic


class ConsumerDevice(typing_extensions.TypedDict):
    """
    Consumer device information provided by merchant
    """

    session_id: typing_extensions.NotRequired[str]
    """
    The unique session identifier of the device that was created by the client. It can be up to 128 characters long and can contain only the following characters: uppercase and lowercase Roman letters, digits, underscore characters, and hyphens (a?z, A?Z, 0?9, _, -). The session ID should contain at least 16 bytes of randomly generated data.
    """


class _SerializerConsumerDevice(pydantic.BaseModel):
    """
    Serializer for ConsumerDevice handling case conversions
    and file omissions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
        populate_by_name=True,
    )

    session_id: typing.Optional[str] = pydantic.Field(alias="sessionId", default=None)
