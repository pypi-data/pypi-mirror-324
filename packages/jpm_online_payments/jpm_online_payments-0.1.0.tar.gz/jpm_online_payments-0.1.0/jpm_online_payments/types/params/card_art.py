import typing
import typing_extensions
import pydantic


class CardArt(typing_extensions.TypedDict):
    """
    Card art information of a payment card.
    """

    name: typing_extensions.NotRequired[str]
    """
    The name of card art that is used to build virtual replication of actual physical card art.
    """

    type_field: typing_extensions.NotRequired[str]
    """
    The category of card art that is used to build virtual replication of actual physical card art.
    """

    url: typing_extensions.NotRequired[str]
    """
    A reference to a web resource on the internet specifying its location on a computer network and a mechanism for retrieving for the card art that is used to build virtual replication of physical card.
    """


class _SerializerCardArt(pydantic.BaseModel):
    """
    Serializer for CardArt handling case conversions
    and file omissions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
        populate_by_name=True,
    )

    name: typing.Optional[str] = pydantic.Field(alias="name", default=None)
    type_field: typing.Optional[str] = pydantic.Field(alias="type", default=None)
    url: typing.Optional[str] = pydantic.Field(alias="url", default=None)
