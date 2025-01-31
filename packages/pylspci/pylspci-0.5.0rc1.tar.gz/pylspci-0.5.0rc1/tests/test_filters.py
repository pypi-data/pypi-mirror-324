from unittest import TestCase

from pylspci.filters import DeviceFilter, SlotFilter


class TestSlotFilter(TestCase):

    def test_empty(self) -> None:
        f = SlotFilter()
        self.assertIsNone(f.domain)
        self.assertIsNone(f.bus)
        self.assertIsNone(f.device)
        self.assertIsNone(f.function)
        self.assertEqual(
            repr(f),
            'SlotFilter(domain=None, bus=None, device=None, function=None)',
        )

    def test_str(self) -> None:
        self.assertEqual(str(SlotFilter()), '::.')
        self.assertEqual(str(SlotFilter(domain=0xcafe)), 'cafe::.')
        self.assertEqual(
            str(SlotFilter(domain=0xc0ff, bus=0xe, device=0xe, function=7)),
            'c0ff:e:e.7',
        )

    def test_parse(self) -> None:
        self.assertEqual(SlotFilter.parse(''), SlotFilter())
        self.assertEqual(SlotFilter.parse('::.'), SlotFilter())
        self.assertEqual(SlotFilter.parse('*:*:*.*'), SlotFilter())
        self.assertEqual(SlotFilter.parse('4'), SlotFilter(device=4))
        self.assertEqual(SlotFilter.parse('4:'), SlotFilter(bus=4))
        self.assertEqual(SlotFilter.parse('4::'), SlotFilter(domain=4))
        self.assertEqual(SlotFilter.parse('.4'), SlotFilter(function=4))
        self.assertEqual(
            SlotFilter.parse('c0ff:e:e.7'),
            SlotFilter(domain=0xc0ff, bus=0xe, device=0xe, function=7),
        )
        with self.assertRaises(ValueError):
            SlotFilter.parse(':::::')
        with self.assertRaises(ValueError):
            SlotFilter.parse('g')

    def test_eq(self) -> None:
        self.assertEqual(
            SlotFilter(domain=0xc0ff, bus=0xe, device=0xe, function=7),
            SlotFilter(domain=0xc0ff, bus=0xe, device=0xe, function=7),
        )
        self.assertNotEqual(
            SlotFilter(domain=0xc0ff, bus=0xf, device=0xe, function=7),
            SlotFilter(domain=0xc0ff, bus=0xe, device=0xe, function=7),
        )
        self.assertNotEqual(
            SlotFilter(domain=0xc0ff, bus=0xf, device=0xe, function=7),
            'not a filter',
        )


class TestDeviceFilter(TestCase):

    def test_empty(self) -> None:
        f = DeviceFilter()
        self.assertIsNone(f.vendor)
        self.assertIsNone(f.device)
        self.assertIsNone(f.cls)
        self.assertEqual(
            repr(f),
            'DeviceFilter(cls=None, vendor=None, device=None)',
        )

    def test_str(self) -> None:
        self.assertEqual(str(DeviceFilter()), '::')
        self.assertEqual(str(DeviceFilter(vendor=0xcafe)), 'cafe::')
        self.assertEqual(
            str(DeviceFilter(vendor=0xc0ff, device=0xe, cls=0xe)),
            'c0ff:e:e',
        )

    def test_parse(self) -> None:
        self.assertEqual(DeviceFilter.parse(''), DeviceFilter())
        self.assertEqual(DeviceFilter.parse('::'), DeviceFilter())
        self.assertEqual(DeviceFilter.parse('*:*:*'), DeviceFilter())
        self.assertEqual(DeviceFilter.parse('4:'), DeviceFilter(vendor=4))
        self.assertEqual(DeviceFilter.parse(':4'), DeviceFilter(device=4))
        self.assertEqual(DeviceFilter.parse('::4'), DeviceFilter(cls=4))
        self.assertEqual(
            DeviceFilter.parse('c0ff:e:e'),
            DeviceFilter(vendor=0xc0ff, device=0xe, cls=0xe),
        )
        with self.assertRaises(ValueError):
            DeviceFilter.parse(':::::')
        with self.assertRaises(ValueError):
            DeviceFilter.parse('4')
        with self.assertRaises(ValueError):
            DeviceFilter.parse('g')

    def test_eq(self) -> None:
        self.assertEqual(
            DeviceFilter(vendor=0xc0ff, device=0xe, cls=0xe),
            DeviceFilter(vendor=0xc0ff, device=0xe, cls=0xe),
        )
        self.assertNotEqual(
            DeviceFilter(vendor=0xc0ff, device=0xf, cls=0xe),
            DeviceFilter(vendor=0xc0ff, device=0xe, cls=0xe),
        )
        self.assertNotEqual(
            DeviceFilter(vendor=0xc0ff, device=0xe, cls=0xe),
            'not a filter',
        )
