""" Unit test for the SPIReg module. """

import unittest
from typing import cast

from spireg import Entry, Register


class TestSPIReg(unittest.TestCase):
    """ Unit test for the SPIReg module. """
    def setUp(self):
        class ExampleRegisterTypes(Register):
            """ Example register with three fields. """
            FIELD_A: int
            FIELD_B: int
            FIELD_C: int

        self.reg = cast(
            ExampleRegisterTypes,
            Register(
                "EXAMPLE_REG", 0x12, "Example register description.", [
                    Entry("FIELD_A", 1),  # Bit 7: Not used
                    Entry("FIELD_B", 1),  # Bit 6: Example binary flag
                    Entry("FIELD_C", 6, 0x15),  # Bits 5-0: Default value of 0x15
                ]
            )
        )

    def test_default_values(self):
        """ Test the default values of the register and its fields. """
        self.assertEqual(self.reg.FIELD_A, 0)
        self.assertEqual(self.reg.FIELD_B, 0)
        self.assertEqual(self.reg.FIELD_C, 0x15)

    def test_set_get_values(self):
        """ Test setting and getting values of the register and its fields. """
        self.reg.FIELD_B = 1
        self.reg.FIELD_C = 0x1F

        self.assertEqual(self.reg.FIELD_B, 1)
        self.assertEqual(self.reg.FIELD_C, 0x1F)

    def test_register_int_conversion(self):
        """ Test converting the register to an integer. """
        self.reg.FIELD_A = 0
        self.reg.FIELD_B = 1
        self.reg.FIELD_C = 0x1F
        expected_value = (1 << 6) | 0x1F  # FIELD_B is at bit 6, FIELD_C in lower 6 bits
        self.assertEqual(int(self.reg), expected_value)

    def test_string_representation(self):
        """ Test the string representation of the register. """
        expected_str = "Bits: 00010101, FIELD_A: 0, FIELD_B: 0, FIELD_C: 21"
        self.assertEqual(expected_str, str(self.reg))


if __name__ == "__main__":
    unittest.main()
