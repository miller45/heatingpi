import unittest
import valve
from unittest.mock import MagicMock
from unittest.mock import patch
import math
import time


class TestValveClass(unittest.TestCase):

    def test_defaultposition(self):
        v = valve.Valve()
        self.assertEqual(v.current_position, 10)

    def test_defaultdirection(self):
        currtime = math.trunc(time.time() * 1000)
        v = valve.Valve()
        v.update(currtime)
        self.assertEqual(False, v.Relay_State1)
        self.assertEqual(False, v.Relay_State2)
        self.assertEqual("STOP", v.direction)

    def test_colder_direction(self):
        currtime = math.trunc(time.time() * 1000)
        v = valve.Valve()
        v.switchRelay1On()
        v.update(currtime)
        self.assertEqual(True, v.Relay_State1)
        self.assertEqual(False, v.Relay_State2)
        self.assertEqual("COLDER", v.direction)

    def test_hotter_direction(self):
        currtime = math.trunc(time.time() * 1000)
        v = valve.Valve()
        v.switchRelay2On()
        v.update(currtime)
        self.assertEqual(False, v.Relay_State1)
        self.assertEqual(True, v.Relay_State2)
        self.assertEqual("HOTTER", v.direction)

    def test_invalid_direction(self):
        currtime = math.trunc(time.time() * 1000)
        v = valve.Valve()
        v.switchRelay1On()
        v.switchRelay2On()
        v.update(currtime)
        self.assertEqual(True, v.Relay_State1)
        self.assertEqual(True, v.Relay_State2)
        self.assertEqual("INVALID", v.direction)