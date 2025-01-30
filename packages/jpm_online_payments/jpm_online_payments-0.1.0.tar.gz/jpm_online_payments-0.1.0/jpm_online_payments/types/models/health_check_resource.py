import typing
import typing_extensions
import pydantic


class HealthCheckResource(pydantic.BaseModel):
    """
    Contains health check information about a resource
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    status: typing.Optional[typing_extensions.Literal["FAIL", "PASS", "WARN"]] = (
        pydantic.Field(alias="status", default=None)
    )
    """
    General status of all resources
    """
