#!/usr/bin/python3

"""WMI device information"""

from __future__ import annotations
from dataclasses import dataclass
from enum import StrEnum
from typing import Optional, Iterable
from pathlib import Path
from os import scandir


class WMIDeviceType(StrEnum):
    """Type of an WMI device"""
    DATABLOCK = "Data"
    METHOD = "Method"
    EVENT = "Event"


def wmi_bus_devices(bus_path: Path = Path('/sys/bus/wmi/devices')) -> Iterable[Path]:
    """Scan for WMI devices on the WMI bus"""
    try:
        with scandir(bus_path) as directory:
            for entry in directory:
                if entry.is_dir():
                    yield Path(entry.path)
    except FileNotFoundError:
        pass


@dataclass(frozen=True, slots=True)
class WMIDevice:
    """WMI device information"""

    guid: str

    device_type: WMIDeviceType

    device_id: str

    instances: int

    expensive: bool

    setable: Optional[bool]

    driver: Optional[str]

    path: Path

    @classmethod
    def from_sysfs(cls, path: Path) -> WMIDevice:
        """Parse WMI device information from sysfs"""
        setable = None

        with (path / 'guid').open('r', encoding='ascii') as fd:
            guid = fd.read().rstrip()

        with (path / 'instance_count').open('r', encoding='ascii') as fd:
            instances = int(fd.read())

        with (path / 'expensive').open('r', encoding='ascii') as fd:
            expensive = int(fd.read()) != 0

        try:
            driver = (path / 'driver').readlink().name
        except FileNotFoundError:
            driver = None

        try:
            with (path / 'notify_id').open('r', encoding='ascii') as fd:
                device_id = fd.read().rstrip()
                device_type = WMIDeviceType.EVENT
        except FileNotFoundError:
            with (path / 'object_id').open('r', encoding='ascii') as fd:
                device_id = fd.read().rstrip()

            try:
                with (path / 'setable').open('r', encoding='ascii') as fd:
                    setable = int(fd.read()) != 0
                    device_type = WMIDeviceType.DATABLOCK
            except FileNotFoundError:
                device_type = WMIDeviceType.METHOD

        return cls(
            guid=guid,
            device_type=device_type,
            device_id=device_id,
            instances=instances,
            expensive=expensive,
            setable=setable,
            driver=driver,
            path=path
        )

    def get_acpi_path(self) -> str:
        """Get path of the ACPI method associated with this WMI device"""
        device_path = self.path.resolve() / '..' / 'device'

        with (device_path / 'firmware_node' / 'path').open('r', encoding='ascii') as fd:
            acpi_path = fd.read().rstrip()

            match self.device_type:
                case WMIDeviceType.METHOD:
                    return f'{acpi_path}.WM{self.device_id}'
                case WMIDeviceType.DATABLOCK:
                    return f'{acpi_path}.WQ{self.device_id}'
                case WMIDeviceType.EVENT:
                    return f'{acpi_path}._WED'
