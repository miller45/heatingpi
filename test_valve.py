import unittest
import valve
from unittest.mock import MagicMock
from unittest.mock import patch

class TestValveClass(unittest.TestCase):

    def test_upper(self):
        v = valve.Valve()
        self.assertEqual(v.current_position,10)