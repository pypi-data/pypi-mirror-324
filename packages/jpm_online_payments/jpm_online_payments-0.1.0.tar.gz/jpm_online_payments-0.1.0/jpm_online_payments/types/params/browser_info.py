import typing
import typing_extensions
import pydantic


class BrowserInfo(typing_extensions.TypedDict):
    """
    Browser Information of the consumer
    """

    browser_accept_header: typing_extensions.NotRequired[str]
    """
    Exact content of the HTTP accept headers as sent to the 3DS Requestor from the Cardholder's browser.
    """

    browser_color_depth: typing_extensions.NotRequired[str]
    """
    Codifies the bit depth of the color palette for displaying images, in bits per pixel. Obtained from Cardholder browser using the screen colorDepth property. The field is limited to 1-2 characters.
    """

    browser_language: typing_extensions.NotRequired[str]
    """
    Codifies the method of communication, either spoken or written, consisting of the use of words in a structured and conventional way. The gold (master) set of values is defined by the International Standards Organization in ISO standard 639-3. In this context, this is the language the device owner has set in the device settings.
    """

    browser_screen_height: typing_extensions.NotRequired[str]
    """
    Total height of the Cardholder's screen in pixels.
    """

    browser_screen_width: typing_extensions.NotRequired[str]
    """
    Total width of the Cardholder's screen in pixels.
    """

    browser_user_agent: typing_extensions.NotRequired[str]
    """
    Exact content of the HTTP user-agent header. The field is limited to maximum 2048 characters.
    """

    challenge_window_size: typing_extensions.NotRequired[
        typing_extensions.Literal[
            "250_400", "390_400", "500_600", "600_400", "FULL_SCREEN"
        ]
    ]
    """
    Dimensions of the challenge window that has been displayed to the Cardholder. The ACS shall reply with content that is formatted to appropriately render in this window to provide the best possible user experience.
    """

    device_ip_address: typing_extensions.NotRequired[str]
    """
    A unique string of numbers separated by periods that identifies each device using the Internet Protocol (IP) to communicate over a network.  An IP address is assigned to every single computer, printer, switch, router or any other device that is part of a TCP/IP-based network which allows users to send and receive data. The numerals in an IP address are divided into two parts:  1) The network part specifies which networks this address belongs to and 2) The host part further pinpoints the exact location. In this context, this is the IP address of the devices associated with the transaction.
    """

    device_local_time_zone: typing_extensions.NotRequired[str]
    """
    Represents a unique code assigned by the firm for a geographical area that observes a uniform standard time for legal, commercial, and social purposes. In this context, this is the local time the device owner has set in the device settings.
    """

    java_enabled: typing_extensions.NotRequired[bool]
    """
    Boolean that represents the ability of the cardholder browser to execute Java.
    """

    java_script_enabled: typing_extensions.NotRequired[bool]
    """
    Indicates if the device's application software, used to communicate between users of the Internet's World Wide Web, allows JavaScript.
    """


class _SerializerBrowserInfo(pydantic.BaseModel):
    """
    Serializer for BrowserInfo handling case conversions
    and file omissions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
        populate_by_name=True,
    )

    browser_accept_header: typing.Optional[str] = pydantic.Field(
        alias="browserAcceptHeader", default=None
    )
    browser_color_depth: typing.Optional[str] = pydantic.Field(
        alias="browserColorDepth", default=None
    )
    browser_language: typing.Optional[str] = pydantic.Field(
        alias="browserLanguage", default=None
    )
    browser_screen_height: typing.Optional[str] = pydantic.Field(
        alias="browserScreenHeight", default=None
    )
    browser_screen_width: typing.Optional[str] = pydantic.Field(
        alias="browserScreenWidth", default=None
    )
    browser_user_agent: typing.Optional[str] = pydantic.Field(
        alias="browserUserAgent", default=None
    )
    challenge_window_size: typing.Optional[
        typing_extensions.Literal[
            "250_400", "390_400", "500_600", "600_400", "FULL_SCREEN"
        ]
    ] = pydantic.Field(alias="challengeWindowSize", default=None)
    device_ip_address: typing.Optional[str] = pydantic.Field(
        alias="deviceIPAddress", default=None
    )
    device_local_time_zone: typing.Optional[str] = pydantic.Field(
        alias="deviceLocalTimeZone", default=None
    )
    java_enabled: typing.Optional[bool] = pydantic.Field(
        alias="javaEnabled", default=None
    )
    java_script_enabled: typing.Optional[bool] = pydantic.Field(
        alias="javaScriptEnabled", default=None
    )
