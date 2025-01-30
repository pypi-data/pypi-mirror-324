import typing
import typing_extensions
import pydantic

from .application_info import ApplicationInfo
from .peripheral_device_type import PeripheralDeviceType


class Device(pydantic.BaseModel):
    """
    Terminal Information used for card prersent transaction.
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    application_info: typing.Optional[ApplicationInfo] = pydantic.Field(
        alias="applicationInfo", default=None
    )
    """
    Terminal Application Information
    """
    attendance: typing.Optional[
        typing_extensions.Literal["ATTENDED", "NO_TERMINAL", "UNATTENDED"]
    ] = pydantic.Field(alias="attendance", default=None)
    """
    Codifies the presense of a worker at the merchant's location at the point of sale terminal for the transaction.
    """
    capabilities: typing.Optional[
        typing.List[
            typing_extensions.Literal[
                "BARCODE",
                "EMV_CONTACT",
                "EMV_CONTACTLESS",
                "KEYED",
                "MAGSTRIPE",
                "MAGSTRIPE_CHIP",
                "MAGSTRIPE_KEY",
                "MAGSTRIPE_KEY_CHIP",
                "MOTO",
                "SWIPE",
            ]
        ]
    ] = pydantic.Field(alias="capabilities", default=None)
    """
    List of capability code that codifies the ability of the point of sale device to electronically read account numbers and expiration dates from payment medium.  The terminal should reflect the highest level of capability. For example, if the terminal is both chip and magnetic stripe read capable, it should be identified as a chip-capable terminal.
    """
    device_id: typing.Optional[str] = pydantic.Field(alias="deviceId", default=None)
    """
    A unique system generated number to identify an occurrence of a record in Terminal Device table.
    """
    location: typing.Optional[
        typing_extensions.Literal["NO_TERMINAL_USED", "OFF_PREMISE", "ON_PREMISE"]
    ] = pydantic.Field(alias="location", default=None)
    """
    Indicates where the terminal was located.
    """
    peripheral_device_type: typing.Optional[PeripheralDeviceType] = pydantic.Field(
        alias="peripheralDeviceType", default=None
    )
    """
    Peripheral Device Information
    """
    pin_capability: typing.Optional[
        typing_extensions.Literal["NO_PIN", "PIN_DOWN", "PIN_ELIGIBLE", "UNKNOWN"]
    ] = pydantic.Field(alias="pinCapability", default=None)
    """
    Codifies the capability of a merchant's terminal or an ATM to accept Personal Identification Numbers (PINs).
    """
    terminal_device_serial_number: typing.Optional[str] = pydantic.Field(
        alias="terminalDeviceSerialNumber", default=None
    )
    """
    A unique identifier issued to each point of sale terminal device by the manufacturer for identification and inventory purposes.
    """
    terminal_id: typing.Optional[str] = pydantic.Field(alias="terminalId", default=None)
    """
    Identifies a unique occurrence of the terminal used for the transaction.
    """
    vendor_id: typing.Optional[str] = pydantic.Field(alias="vendorId", default=None)
    """
    Identifies a unique occurrence of a client vendor on a clients financial system. This is one of several pieces of data maintained on a clients financial system that may be used in the end to end payment process. A client vendor is an entity who provides goods or services to the client in return for payment.
    """
