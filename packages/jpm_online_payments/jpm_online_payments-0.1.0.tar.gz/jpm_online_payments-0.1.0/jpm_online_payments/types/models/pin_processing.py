import typing
import pydantic


class PinProcessing(pydantic.BaseModel):
    """
    PIN processing information
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    key_sequence_number: typing.Optional[str] = pydantic.Field(
        alias="keySequenceNumber", default=None
    )
    """
    Identifies the number indicating the location of this record in the sorting sequence of the specified data.
    """
    pin_block: typing.Optional[str] = pydantic.Field(alias="pinBlock", default=None)
    """
    Textual block of data used to encapsulate a PIN during processing. The PIN block format defines the content of the PIN block and how it is processed to retrieve the PIN. The PIN block is composed of the PIN, the PIN length, and may contain subset of the account number.
    """
    pinpad_serial_number: typing.Optional[str] = pydantic.Field(
        alias="pinpadSerialNumber", default=None
    )
    """
    A unique identifier issued to each point of sale terminal device by the manufacturer for identification and inventory purposes.
    """
