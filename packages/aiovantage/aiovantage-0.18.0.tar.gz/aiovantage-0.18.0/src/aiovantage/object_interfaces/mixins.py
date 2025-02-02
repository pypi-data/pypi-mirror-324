"""Field definitions for various mixins, aka 'Interface Classes'."""

from dataclasses import dataclass, field


@dataclass
class ShadeOrientation:
    """Shade orientation field support."""

    shade_orientation: str | None = field(
        default=None,
        repr=False,
        metadata={"type": "Attribute"},
    )


@dataclass
class ShadeType:
    """Shade type field support."""

    shade_type: str | None = field(
        default=None,
        repr=False,
        metadata={"type": "Attribute"},
    )
