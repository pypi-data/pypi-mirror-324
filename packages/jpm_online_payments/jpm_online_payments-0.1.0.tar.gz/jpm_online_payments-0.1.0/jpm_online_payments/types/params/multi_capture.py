import typing
import typing_extensions
import pydantic


class MultiCapture(typing_extensions.TypedDict):
    """
    Split Shipment Information
    """

    is_final_capture: typing_extensions.NotRequired[bool]
    """
    Indicates if it is the final shipment associated with a single authorization.
    """

    multi_capture_record_count: typing_extensions.NotRequired[int]
    """
    Enumerates the quantity of records in a data object that is processed or transmitted. In this context, this is the total number of expected shipments associated with a single authorization.
    """

    multi_capture_sequence_number: typing_extensions.NotRequired[str]
    """
    Identifies the number indicating the location of this record in the sorting sequence of the specified data.
    """


class _SerializerMultiCapture(pydantic.BaseModel):
    """
    Serializer for MultiCapture handling case conversions
    and file omissions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
        populate_by_name=True,
    )

    is_final_capture: typing.Optional[bool] = pydantic.Field(
        alias="isFinalCapture", default=None
    )
    multi_capture_record_count: typing.Optional[int] = pydantic.Field(
        alias="multiCaptureRecordCount", default=None
    )
    multi_capture_sequence_number: typing.Optional[str] = pydantic.Field(
        alias="multiCaptureSequenceNumber", default=None
    )
