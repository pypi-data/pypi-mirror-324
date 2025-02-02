"""Introspection interface (IIntrospection) method definitions."""

from .get_interfaces import GetInterfaces
from .get_sys_info import GetSysInfo
from .get_types import GetTypes
from .get_version import GetVersion

__all__ = [
    "GetInterfaces",
    "GetSysInfo",
    "GetTypes",
    "GetVersion",
]
