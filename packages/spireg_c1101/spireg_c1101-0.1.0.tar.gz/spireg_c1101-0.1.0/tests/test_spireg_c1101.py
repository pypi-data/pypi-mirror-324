""" Unit test for the SPIReg module. """

import unittest

from spireg_c1101 import configuration_register


class TestSPIReg(unittest.TestCase):
    """ Unit test for the SPIReg module. """
    def setUp(self):
        pass

    def test_getting_and_setting(self):
        """ Test getting and setting some values of a register. """
        bscfg = configuration_register.BSCFG
        bscfg.value = 0x15
        self.assertEqual(bscfg.BS_PRE_KI, 0)
        self.assertEqual(bscfg.BS_PRE_KP, 1)
        self.assertEqual(bscfg.BS_POST_KI, 0)
        self.assertEqual(bscfg.BS_POST_KP, 1)
        self.assertEqual(bscfg.BS_LIMIT, 1)
        bscfg.BS_PRE_KI = 1
        self.assertEqual(bscfg.value, 0x55)


if __name__ == "__main__":
    unittest.main()
