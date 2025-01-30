import typing
import pydantic


class PeripheralDeviceType(pydantic.BaseModel):
    """
    Peripheral Device Information
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    card_magnetic_stripe: typing.Optional[bool] = pydantic.Field(
        alias="cardMagneticStripe", default=None
    )
    """
    Indicate the card is magnetic stripe enabled.
    """
    external_card_chip_reader: typing.Optional[bool] = pydantic.Field(
        alias="externalCardChipReader", default=None
    )
    """
    Indicate if card is enabled with external chip reader for capturing the card details
    """
    external_contactless_card_reader: typing.Optional[bool] = pydantic.Field(
        alias="externalContactlessCardReader", default=None
    )
    """
    Indicate the card is enable with external contactless card reader
    """
    external_pin_pad: typing.Optional[bool] = pydantic.Field(
        alias="externalPinPad", default=None
    )
    """
    Indicate the terminal device support external PIN pad, that allows the consumer to enter PIN during authentication.
    """
    internal_card_chip_reader: typing.Optional[bool] = pydantic.Field(
        alias="internalCardChipReader", default=None
    )
    """
    Indicate if card is enabled with internal chip reader for capturing the card details
    """
    internal_contactless_card_reader: typing.Optional[bool] = pydantic.Field(
        alias="internalContactlessCardReader", default=None
    )
    """
    Indicate the card is enable with internal contactless card reader
    """
    internal_pin_pad: typing.Optional[bool] = pydantic.Field(
        alias="internalPinPad", default=None
    )
    """
    Indicate the terminal device has Internal PIN pad, that allows the consumer to enter PIN during authentication.
    """
