import unittest
import arduino
from unittest.mock import MagicMock
from unittest.mock import patch
import math
import time

FULLTURNTIME = 120



class TestArduinoClass(unittest.TestCase):

    def test_defaultposition(self):
        v = arduino.Arduino("/dev/ttyDummy")
        

   