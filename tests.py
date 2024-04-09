import unittest
from main import CurrencyConverter


class TestCurrencyConverter(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Inițializează clasa
        cls.converter = CurrencyConverter()

    def testSameCurrency(self):
        self.assertEqual(self.converter.convert(1, 'USD', 'USD'), 1)

    def testDifferentRate(self):
        self.converter.exchange_rates['EUR'] = 0.93  # Pp rata USD->EUR este 0.93 pentru test
        self.assertAlmostEqual(self.converter.convert(1, 'USD', 'EUR'), 0.93)

    def testInverseRate(self):
        self.converter.exchange_rates['EUR'] = 0.93  # Pp rata USD->EUR este 0.93 pentru test
        self.assertAlmostEqual(self.converter.convert(1, 'EUR', 'USD'), 1 / 0.93)

    def testUnknownCurrency(self):
        self.assertRaises(ValueError, self.converter.convert, 1, 'USD', '___')

    def testInvalidAmount(self):
        self.assertRaises(ValueError, self.converter.convert, 'invalid', 'USD', 'EUR')

    def testZeroAmount(self):
        self.assertEqual(self.converter.convert(0, 'USD', 'EUR'), 0)

    def testNegativeAmount(self):
        self.assertRaises(ValueError, self.converter.convert, -1, 'USD', 'EUR')


if __name__ == '__main__':
    unittest.main()
