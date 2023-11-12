#!/usr/bin/python3

"""Test for WMI device handling"""

from unittest import TestCase
from pathlib import Path
from tempfile import TemporaryDirectory
from lswmi.device import WMIDevice, WMIDeviceType, wmi_bus_devices


def create_file(path: Path, content: str) -> None:
    """Create file with specific content"""
    with path.open('x', encoding='ascii') as fd:
        fd.write(f'{content}\n')


def create_wmi_device(device: WMIDevice) -> None:
    """Create WMI device sysfs structure"""
    device_dir = Path(device.path)
    device_dir.mkdir(mode=0o755)

    create_file((device_dir / 'guid'), device.guid)
    create_file((device_dir / 'expensive'), int(device.expensive))
    create_file((device_dir / 'instance_count'), device.instances)

    if device.device_type == WMIDeviceType.EVENT:
        create_file((device_dir / 'notify_id'), device.device_id)
    else:
        create_file((device_dir / 'object_id'), device.device_id)
        if device.device_type == WMIDeviceType.DATABLOCK:
            create_file((device_dir / 'setable'), int(device.setable))

    if device.driver is not None:
        (device_dir / 'driver').symlink_to(f'../../drivers/{device.driver}')


class WmiDeviceTest(TestCase):
    """Tests for WMI device handling"""

    def setUp(self):
        """Prepare fake WMI bus directory"""
        bus_path = Path(self.enterContext(TemporaryDirectory()))
        self.device_path = bus_path / 'devices'
        self.device_path.mkdir(mode=0o755)

        self.bmof_device = WMIDevice(
            guid='05901221-D566-11D1-B2F0-00A0C9062910',
            device_type=WMIDeviceType.DATABLOCK,
            device_id='MO',
            instances=1,
            expensive=False,
            setable=False,
            driver='wmi-bmof',
            path=(self.device_path / '05901221-D566-11D1-B2F0-00A0C9062910')
        )
        create_wmi_device(self.bmof_device)

        self.bmof_device_duplicate = WMIDevice(
            guid='05901221-D566-11D1-B2F0-00A0C9062910',
            device_type=WMIDeviceType.DATABLOCK,
            device_id='MO',
            instances=1,
            expensive=False,
            setable=False,
            driver='wmi-bmof',
            path=(self.device_path / '05901221-D566-11D1-B2F0-00A0C9062910-1')
        )
        create_wmi_device(self.bmof_device_duplicate)

        self.ddv_device = WMIDevice(
            guid='8A42EA14-4F2A-FD45-6422-0087F7A7E608',
            device_type=WMIDeviceType.METHOD,
            device_id='DV',
            instances=1,
            expensive=False,
            setable=None,
            driver='dell-wmi-ddv',
            path=(self.device_path / '8A42EA14-4F2A-FD45-6422-0087F7A7E608')
        )
        create_wmi_device(self.ddv_device)

        self.eeepc_device = WMIDevice(
            guid='ABBC0F72-8EA1-11D1-00A0-C90629100000',
            device_type=WMIDeviceType.EVENT,
            device_id='D2',
            instances=1,
            expensive=False,
            setable=None,
            driver=None,
            path=(self.device_path / 'ABBC0F72-8EA1-11D1-00A0-C90629100000')
        )
        create_wmi_device(self.eeepc_device)

    def test_simple_datablock(self) -> None:
        """Test detection of an simple WMI datablock device"""
        device = WMIDevice.from_sysfs(
            self.device_path / '05901221-D566-11D1-B2F0-00A0C9062910'
        )

        self.assertEqual(device, self.bmof_device)

    def test_simple_method(self) -> None:
        """Test detection of an simple WMI method device"""
        device = WMIDevice.from_sysfs(
            self.device_path / '8A42EA14-4F2A-FD45-6422-0087F7A7E608'
        )

        self.assertEqual(device, self.ddv_device)

    def test_simple_event(self) -> None:
        """Test detection of an simple WMI event device"""
        device = WMIDevice.from_sysfs(
            self.device_path / 'ABBC0F72-8EA1-11D1-00A0-C90629100000'
        )

        self.assertEqual(device, self.eeepc_device)

    def test_duplicate(self) -> None:
        """Test detection of an WMI device with an duplicate GUID"""
        device = WMIDevice.from_sysfs(
            self.device_path / '05901221-D566-11D1-B2F0-00A0C9062910-1'
        )

        self.assertEqual(device, self.bmof_device_duplicate)

    def test_detection(self) -> None:
        """Test detection of all WMI devices"""
        devices = list(wmi_bus_devices(self.device_path.as_posix()))

        self.assertIn(self.bmof_device.path, devices)
        self.assertIn(self.bmof_device_duplicate.path, devices)
        self.assertIn(self.ddv_device.path, devices)
        self.assertIn(self.eeepc_device.path, devices)
        self.assertEqual(len(devices), 4)

    def test_detection_nondir(self) -> None:
        """Test if device detection ignores files"""
        create_file(
            self.device_path / '05901221-D566-11D1-B2F0-00A0C9062910-2',
            'dummy'
        )

        with self.subTest("Device detection did not ignore file"):
            self.test_detection()
