import typing
import typing_extensions
import pydantic


class PeripheralDeviceType(typing_extensions.TypedDict):
    """
    Peripheral Device Information
    """

    card_magnetic_stripe: typing_extensions.NotRequired[bool]
    """
    Indicate the card is magnetic stripe enabled.
    """

    external_card_chip_reader: typing_extensions.NotRequired[bool]
    """
    Indicate if card is enabled with external chip reader for capturing the card details
    """

    external_contactless_card_reader: typing_extensions.NotRequired[bool]
    """
    Indicate the card is enable with external contactless card reader
    """

    external_pin_pad: typing_extensions.NotRequired[bool]
    """
    Indicate the terminal device support external PIN pad, that allows the consumer to enter PIN during authentication.
    """

    internal_card_chip_reader: typing_extensions.NotRequired[bool]
    """
    Indicate if card is enabled with internal chip reader for capturing the card details
    """

    internal_contactless_card_reader: typing_extensions.NotRequired[bool]
    """
    Indicate the card is enable with internal contactless card reader
    """

    internal_pin_pad: typing_extensions.NotRequired[bool]
    """
    Indicate the terminal device has Internal PIN pad, that allows the consumer to enter PIN during authentication.
    """


class _SerializerPeripheralDeviceType(pydantic.BaseModel):
    """
    Serializer for PeripheralDeviceType handling case conversions
    and file omissions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
        populate_by_name=True,
    )

    card_magnetic_stripe: typing.Optional[bool] = pydantic.Field(
        alias="cardMagneticStripe", default=None
    )
    external_card_chip_reader: typing.Optional[bool] = pydantic.Field(
        alias="externalCardChipReader", default=None
    )
    external_contactless_card_reader: typing.Optional[bool] = pydantic.Field(
        alias="externalContactlessCardReader", default=None
    )
    external_pin_pad: typing.Optional[bool] = pydantic.Field(
        alias="externalPinPad", default=None
    )
    internal_card_chip_reader: typing.Optional[bool] = pydantic.Field(
        alias="internalCardChipReader", default=None
    )
    internal_contactless_card_reader: typing.Optional[bool] = pydantic.Field(
        alias="internalContactlessCardReader", default=None
    )
    internal_pin_pad: typing.Optional[bool] = pydantic.Field(
        alias="internalPinPad", default=None
    )
