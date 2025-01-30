import typing
import typing_extensions
import pydantic


class ApplicationInfo(pydantic.BaseModel):
    """
    Terminal Application Information
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    classification_type: typing.Optional[
        typing_extensions.Literal[
            "CLASS_A",
            "CLASS_B",
            "GATEWAY",
            "INTEGRATOR",
            "MERCHANT_APPLICATION",
            "MIDDLEWARE",
            "NON_COMPLIANT",
        ]
    ] = pydantic.Field(alias="classificationType", default=None)
    """
    Codifies the compliance supported by point of sale terminal.
    """
    device_type: typing.Optional[
        typing_extensions.Literal[
            "ANDROID PHONE", "ANDROID TABLET", "IPAD", "IPHONE", "OTHER"
        ]
    ] = pydantic.Field(alias="deviceType", default=None)
    """
    Codifies the mechanism used to provide payment details at merchant's terminal for the transaction. Null value indicates that device type is not provided.
    """
    mobile_device_type: typing.Optional[
        typing_extensions.Literal["COTS_NO_PIN", "COTS_PIN", "MPOS_NO_PIN", "MPOS_PIN"]
    ] = pydantic.Field(alias="mobileDeviceType", default=None)
    """
    Codifies the category of mobile  device used by point of sale terminal.
    """
