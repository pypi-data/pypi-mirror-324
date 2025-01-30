import typing
import typing_extensions
import pydantic


class PinProcessing(typing_extensions.TypedDict):
    """
    PIN processing information
    """

    key_sequence_number: typing_extensions.NotRequired[str]
    """
    Identifies the number indicating the location of this record in the sorting sequence of the specified data.
    """

    pin_block: typing_extensions.NotRequired[str]
    """
    Textual block of data used to encapsulate a PIN during processing. The PIN block format defines the content of the PIN block and how it is processed to retrieve the PIN. The PIN block is composed of the PIN, the PIN length, and may contain subset of the account number.
    """

    pinpad_serial_number: typing_extensions.NotRequired[str]
    """
    A unique identifier issued to each point of sale terminal device by the manufacturer for identification and inventory purposes.
    """


class _SerializerPinProcessing(pydantic.BaseModel):
    """
    Serializer for PinProcessing handling case conversions
    and file omissions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
        populate_by_name=True,
    )

    key_sequence_number: typing.Optional[str] = pydantic.Field(
        alias="keySequenceNumber", default=None
    )
    pin_block: typing.Optional[str] = pydantic.Field(alias="pinBlock", default=None)
    pinpad_serial_number: typing.Optional[str] = pydantic.Field(
        alias="pinpadSerialNumber", default=None
    )
