import typing
import typing_extensions
import pydantic


class PaymentMetadata(typing_extensions.TypedDict):
    """
    Additional metadata information merchant send during payment request
    """

    metadata_attribute: typing_extensions.NotRequired[str]
    """
    Specifies the label of the attribute associated with a data element when used in a key-value pair.
    """

    metadata_attribute_value: typing_extensions.NotRequired[str]
    """
    Provides textual information about the Value assigned to a data element when used in a key-value pair.
    """


class _SerializerPaymentMetadata(pydantic.BaseModel):
    """
    Serializer for PaymentMetadata handling case conversions
    and file omissions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
        populate_by_name=True,
    )

    metadata_attribute: typing.Optional[str] = pydantic.Field(
        alias="metadataAttribute", default=None
    )
    metadata_attribute_value: typing.Optional[str] = pydantic.Field(
        alias="metadataAttributeValue", default=None
    )
