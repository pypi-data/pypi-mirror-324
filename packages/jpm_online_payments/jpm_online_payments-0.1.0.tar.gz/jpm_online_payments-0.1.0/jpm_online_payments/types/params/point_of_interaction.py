import typing
import typing_extensions
import pydantic

from .device import Device, _SerializerDevice
from .in_person import InPerson, _SerializerInPerson


class PointOfInteraction(typing_extensions.TypedDict):
    """
    In store payment Information
    """

    device: typing_extensions.NotRequired[Device]
    """
    Terminal Information used for card prersent transaction.
    """

    in_person: typing_extensions.NotRequired[InPerson]
    """
    Card present information
    """


class _SerializerPointOfInteraction(pydantic.BaseModel):
    """
    Serializer for PointOfInteraction handling case conversions
    and file omissions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
        populate_by_name=True,
    )

    device: typing.Optional[_SerializerDevice] = pydantic.Field(
        alias="device", default=None
    )
    in_person: typing.Optional[_SerializerInPerson] = pydantic.Field(
        alias="inPerson", default=None
    )
