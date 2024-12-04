import unittest
from helpers import convert_8_to_10_digits


class TestFunctionality(unittest.TestCase):

    def setUp(self):
        self.local_number = "97970000"
        self.local_number_with_229 = "+22997970000"
        self.france_number = "+33109758351"
        self.usa_number = "+19512390523"

    def tearDown(self):
        del self.local_number

    def test_convertion_local_number(self):
        self.assertListEqual(convert_8_to_10_digits(self.local_number), ["0197970000"])

    def test_convertion_local_number_with_229(self):
        self.assertListEqual(convert_8_to_10_digits(self.local_number_with_229), ["+2290197970000", "0197970000"])

    def test_convertion_france_number(self):
        self.assertEqual(convert_8_to_10_digits(self.france_number), False)

    def test_convertion_usa_number(self):
        self.assertEqual(convert_8_to_10_digits(self.usa_number), False)


# TODO: Add process_individual_vcard Testing


if __name__ == "__main__":
    unittest.main()
