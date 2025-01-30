import typing
import pydantic


class StoreandForward(pydantic.BaseModel):
    """
    Store and Forward transaction information.
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    is_store_and_forward: typing.Optional[bool] = pydantic.Field(
        alias="isStoreAndForward", default=None
    )
    """
    Indicate the terminal captured data to be stored internally and forward to internal processor.
    """
