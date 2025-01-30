import typing
import typing_extensions
import pydantic


class ApplicationInfo(typing_extensions.TypedDict):
    """
    Terminal Application Information
    """

    classification_type: typing_extensions.NotRequired[
        typing_extensions.Literal[
            "CLASS_A",
            "CLASS_B",
            "GATEWAY",
            "INTEGRATOR",
            "MERCHANT_APPLICATION",
            "MIDDLEWARE",
            "NON_COMPLIANT",
        ]
    ]
    """
    Codifies the compliance supported by point of sale terminal.
    """

    device_type: typing_extensions.NotRequired[
        typing_extensions.Literal[
            "ANDROID PHONE", "ANDROID TABLET", "IPAD", "IPHONE", "OTHER"
        ]
    ]
    """
    Codifies the mechanism used to provide payment details at merchant's terminal for the transaction. Null value indicates that device type is not provided.
    """

    mobile_device_type: typing_extensions.NotRequired[
        typing_extensions.Literal["COTS_NO_PIN", "COTS_PIN", "MPOS_NO_PIN", "MPOS_PIN"]
    ]
    """
    Codifies the category of mobile  device used by point of sale terminal.
    """


class _SerializerApplicationInfo(pydantic.BaseModel):
    """
    Serializer for ApplicationInfo handling case conversions
    and file omissions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
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
    device_type: typing.Optional[
        typing_extensions.Literal[
            "ANDROID PHONE", "ANDROID TABLET", "IPAD", "IPHONE", "OTHER"
        ]
    ] = pydantic.Field(alias="deviceType", default=None)
    mobile_device_type: typing.Optional[
        typing_extensions.Literal["COTS_NO_PIN", "COTS_PIN", "MPOS_NO_PIN", "MPOS_PIN"]
    ] = pydantic.Field(alias="mobileDeviceType", default=None)
