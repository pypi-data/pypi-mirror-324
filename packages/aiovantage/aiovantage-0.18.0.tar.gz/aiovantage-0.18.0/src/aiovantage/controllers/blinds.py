"""Controller holding and managing Vantage blinds."""

from aiovantage.objects import (
    QISBlind,
    QubeBlind,
    RelayBlind,
    SomfyRS485ShadeChild,
    SomfyURTSI2ShadeChild,
)

from .base import BaseController

BlindTypes = (
    QISBlind | QubeBlind | RelayBlind | SomfyRS485ShadeChild | SomfyURTSI2ShadeChild
)


class BlindsController(BaseController[BlindTypes]):
    """Controller holding and managing Vantage blinds."""

    vantage_types = (
        "QISBlind",
        "QubeBlind",
        "RelayBlind",
        "Somfy.RS-485_Shade_CHILD",
        "Somfy.URTSI_2_Shade_CHILD",
    )
