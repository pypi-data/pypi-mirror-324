import typing
import pydantic


class Information(pydantic.BaseModel):
    """
    A list of informational messages
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    code_field: typing.Optional[str] = pydantic.Field(alias="code", default=None)
    """
    Codifies the instruction provided in the application
    """
    message: typing.Optional[str] = pydantic.Field(alias="message", default=None)
    """
    Long explanation of the instruction provided in the application
    """
