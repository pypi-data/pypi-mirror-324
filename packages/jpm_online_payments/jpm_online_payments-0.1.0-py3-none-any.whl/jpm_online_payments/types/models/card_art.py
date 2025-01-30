import typing
import pydantic


class CardArt(pydantic.BaseModel):
    """
    Card art information of a payment card.
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    name: typing.Optional[str] = pydantic.Field(alias="name", default=None)
    """
    The name of card art that is used to build virtual replication of actual physical card art.
    """
    type_field: typing.Optional[str] = pydantic.Field(alias="type", default=None)
    """
    The category of card art that is used to build virtual replication of actual physical card art.
    """
    url: typing.Optional[str] = pydantic.Field(alias="url", default=None)
    """
    A reference to a web resource on the internet specifying its location on a computer network and a mechanism for retrieving for the card art that is used to build virtual replication of physical card.
    """
