import typing
import pydantic


class ConsumerDevice(pydantic.BaseModel):
    """
    Consumer device information provided by merchant
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    session_id: typing.Optional[str] = pydantic.Field(alias="sessionId", default=None)
    """
    The unique session identifier of the device that was created by the client. It can be up to 128 characters long and can contain only the following characters: uppercase and lowercase Roman letters, digits, underscore characters, and hyphens (a?z, A?Z, 0?9, _, -). The session ID should contain at least 16 bytes of randomly generated data.
    """
