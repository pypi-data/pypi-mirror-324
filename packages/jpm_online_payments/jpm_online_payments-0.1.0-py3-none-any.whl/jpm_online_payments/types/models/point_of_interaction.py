import typing
import pydantic

from .device import Device
from .in_person import InPerson


class PointOfInteraction(pydantic.BaseModel):
    """
    In store payment Information
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    device: typing.Optional[Device] = pydantic.Field(alias="device", default=None)
    """
    Terminal Information used for card prersent transaction.
    """
    in_person: typing.Optional[InPerson] = pydantic.Field(
        alias="inPerson", default=None
    )
    """
    Card present information
    """
