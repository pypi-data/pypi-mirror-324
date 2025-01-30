import typing
import typing_extensions
import pydantic


class StoreandForward(typing_extensions.TypedDict):
    """
    Store and Forward transaction information.
    """

    is_store_and_forward: typing_extensions.NotRequired[bool]
    """
    Indicate the terminal captured data to be stored internally and forward to internal processor.
    """


class _SerializerStoreandForward(pydantic.BaseModel):
    """
    Serializer for StoreandForward handling case conversions
    and file omissions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
        populate_by_name=True,
    )

    is_store_and_forward: typing.Optional[bool] = pydantic.Field(
        alias="isStoreAndForward", default=None
    )
