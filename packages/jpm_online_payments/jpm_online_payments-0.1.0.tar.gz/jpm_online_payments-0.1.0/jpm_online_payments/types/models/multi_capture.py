import typing
import pydantic


class MultiCapture(pydantic.BaseModel):
    """
    Split Shipment Information
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    is_final_capture: typing.Optional[bool] = pydantic.Field(
        alias="isFinalCapture", default=None
    )
    """
    Indicates if it is the final shipment associated with a single authorization.
    """
    multi_capture_record_count: typing.Optional[int] = pydantic.Field(
        alias="multiCaptureRecordCount", default=None
    )
    """
    Enumerates the quantity of records in a data object that is processed or transmitted. In this context, this is the total number of expected shipments associated with a single authorization.
    """
    multi_capture_sequence_number: typing.Optional[str] = pydantic.Field(
        alias="multiCaptureSequenceNumber", default=None
    )
    """
    Identifies the number indicating the location of this record in the sorting sequence of the specified data.
    """
