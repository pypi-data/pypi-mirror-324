import typing
import typing_extensions
import pydantic


class RiskElement(pydantic.BaseModel):
    """
    Object containing Risk Element information
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    browser_adobe_flash_enabled: typing.Optional[bool] = pydantic.Field(
        alias="browserAdobeFlashEnabled", default=None
    )
    """
    Indicates if the device's application software, used to communicate between users of the Internet's World Wide Web, allows Adobe flash.
    """
    browser_cookies_enabled: typing.Optional[bool] = pydantic.Field(
        alias="browserCookiesEnabled", default=None
    )
    """
    Indicates if the device's application software, used to communicate between users of the Internet's World Wide Web, allows cookies.
    """
    browser_java_script_enabled: typing.Optional[bool] = pydantic.Field(
        alias="browserJavaScriptEnabled", default=None
    )
    """
    Indicates if the device's application software, used to communicate between users of the Internet's World Wide Web, allows JavaScript.
    """
    card_type: typing.Optional[
        typing_extensions.Literal[
            "AP",
            "AX",
            "CC",
            "CR",
            "CZ",
            "DC",
            "DI",
            "EP",
            "IM",
            "JC",
            "MC",
            "MR",
            "NP",
            "PP",
            "SP",
            "VI",
            "VR",
        ]
    ] = pydantic.Field(alias="cardType", default=None)
    """
    Abbreviation of card name
    """
    device_browser_country: typing.Optional[str] = pydantic.Field(
        alias="deviceBrowserCountry", default=None
    )
    """
    Uniquely represents a firm-recognized geopolitical area, including the ISO 3166 alpha 2-character country codes and other firm-created country codes. In this context, this is the country code associated with browser.
    """
    device_browser_language: typing.Optional[str] = pydantic.Field(
        alias="deviceBrowserLanguage", default=None
    )
    """
    Codifies the method of communication, either spoken or written, consisting of the use of words in a structured and conventional way. The gold (master) set of values is defined by the International Standards Organization in ISO standard 639-3. In this context, this is the language the device owner has set in the device settings.
    """
    device_country: typing.Optional[str] = pydantic.Field(
        alias="deviceCountry", default=None
    )
    """
    Codifies the country, a geographic area, that is recognized as an independent political unit in world affairs where the point of sale device was used for a transaction. Null value indicates country code is not provided.
    """
    device_layers: typing.Optional[str] = pydantic.Field(
        alias="deviceLayers", default=None
    )
    """
    Identifies a unique occurrence of an electronic device (and the software) used by the customer to communicate with the Firm or a third party to receive, store, process or send digital information.
    """
    device_local_time_zone: typing.Optional[str] = pydantic.Field(
        alias="deviceLocalTimeZone", default=None
    )
    """
    Represents a unique code assigned by the firm for a geographical area that observes a uniform standard time for legal, commercial, and social purposes. In this context, this is the local time the device owner has set in the device settings.
    """
    device_network_type: typing.Optional[str] = pydantic.Field(
        alias="deviceNetworkType", default=None
    )
    """
    Codifies the categorization of the internet network using the Internet Protocol (IP) Address associated with the party (consumer). This category is assigned by the fraud engine based on the IP address/domain.
    """
    device_proxy_server: typing.Optional[bool] = pydantic.Field(
        alias="deviceProxyServer", default=None
    )
    """
    Indicates if a device uses a proxy server as an intermediary between an endpoint device, such as a computer or mobile device, and the server from which a user or client is making a purchase.
    """
    device_region: typing.Optional[str] = pydantic.Field(
        alias="deviceRegion", default=None
    )
    """
    Codifies a geographic area represented by one or more Countries, States or Provinces. Country, State or Province identifies a geographic area that represents a Firm recognized geopolitical unit. In this context, this is the region associated to the Device Location.
    """
    device_remotely_control_capability: typing.Optional[bool] = pydantic.Field(
        alias="deviceRemotelyControlCapability", default=None
    )
    """
    Indicate if the device placing the order is enabled to use PC Remote software.
    """
    device_timestamp: typing.Optional[str] = pydantic.Field(
        alias="deviceTimestamp", default=None
    )
    """
    Designates the current hour (hh), minute (mm), seconds (ss) and date on the electronic instrument used by a consumer for a payment authorization during the fraud analysis. This may differ from the actual current time if changed by the device owner.
    """
    device_voice_controlled: typing.Optional[bool] = pydantic.Field(
        alias="deviceVoiceControlled", default=None
    )
    """
    Indicate if the device placing the order voice activated (related to mobile devices).
    """
    device_wireless_capability: typing.Optional[bool] = pydantic.Field(
        alias="deviceWirelessCapability", default=None
    )
    """
    Indicate if the device placing the order has capability to connect to internet wirelessly.
    """
    digital_device_type: typing.Optional[str] = pydantic.Field(
        alias="digitalDeviceType", default=None
    )
    """
    The label given to the type of electronic device that can receive, store, process or send digital information that can be used to communicate with a web page.
    """
    fourteen_days_card_record_count: typing.Optional[int] = pydantic.Field(
        alias="fourteenDaysCardRecordCount", default=None
    )
    """
    Enumerates the quantity of records in a data object that is processed or transmitted. In this context, this is the number of cards associated with transaction that the fraud system has recorded.
    """
    fourteen_days_device_record_count: typing.Optional[int] = pydantic.Field(
        alias="fourteenDaysDeviceRecordCount", default=None
    )
    """
    Enumerates the quantity of records in a data object that is processed or transmitted. In this context, this is the record count of the email associated with the transaction that the fraud system has recorded.
    """
    fourteen_days_email_record_count: typing.Optional[int] = pydantic.Field(
        alias="fourteenDaysEmailRecordCount", default=None
    )
    """
    Enumerates the quantity of records in a data object that is processed or transmitted. In this context, this is the record count of the devices associated with the transaction that the fraud system has recorded.
    """
    fourteen_days_transaction_count: typing.Optional[int] = pydantic.Field(
        alias="fourteenDaysTransactionCount", default=None
    )
    """
    Enumerates the occurrences of any transaction within a given period. In this context, this represent how many times the persona has been seen for the merchant in last 14 days.
    """
    fraud_evaluator_transaction_id: typing.Optional[str] = pydantic.Field(
        alias="fraudEvaluatorTransactionId", default=None
    )
    """
    Identifies a unique occurrence of a transaction. In this context, this is the fraud evaluator provided transaction id.
    """
    hashed_digital_device_fingerprint_identifier: typing.Optional[str] = pydantic.Field(
        alias="hashedDigitalDeviceFingerprintIdentifier", default=None
    )
    """
    Identifies a unique occurrence of an electronic device (and the software) used by the customer to communicate with the Firm or a third party to receive, store, process or send digital information. In this context, this identifier consists of the 5 device layers representing the operating system, browser, JavaScript settings, cookie setting and flash settings.
    """
    highest_risk_country: typing.Optional[str] = pydantic.Field(
        alias="highestRiskCountry", default=None
    )
    """
    The portion of a party's address that is the encoded representation of a geographic area representing a country. Tn this context, this represents the country with the highest level of known e-commerce risk, as determined by the US State Department, that has been associated with a particular persona within the last 14 days.
    """
    highest_risk_region: typing.Optional[str] = pydantic.Field(
        alias="highestRiskRegion", default=None
    )
    """
    Codifies a geographic area represented by one or more Countries, States or Provinces. Country, State or Province identifies a geographic area that represents a Firm recognized geopolitical unit. In this context, this is the region which represents the highest level of known e-commerce risk, as determined by the US State Department, that has been associated with a particular persona within the last 14 days.
    """
    mobile_device: typing.Optional[bool] = pydantic.Field(
        alias="mobileDevice", default=None
    )
    """
    Indicate if the device placing the order a mobile device.
    """
    session_match_indicator: typing.Optional[bool] = pydantic.Field(
        alias="sessionMatchIndicator", default=None
    )
    """
    Indicates the Kaptcha session identifier generated by the fraud engine during checkout is validated and matches the session identifier received on the transaction.
    """
    six_hours_transaction_count: typing.Optional[int] = pydantic.Field(
        alias="sixHoursTransactionCount", default=None
    )
    """
    Enumerates the occurrences of any transaction within a given period. In this context, this represent how many times the persona has been seen for the merchant in last 6 hours.
    """
