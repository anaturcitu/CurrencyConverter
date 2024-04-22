import unittest
import json
from unittest.mock import patch, mock_open
from main import CurrencyConverter

class TestCurrencyConverter(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        # Initialize the CurrencyConverter instance
        self.converter = CurrencyConverter()

    def test_same_currency(self):
        self.assertEqual(self.converter.convert(1, 'USD', 'USD'), 1)

    def test_different_rate(self):
        self.converter.exchange_rates['EUR'] = 0.93
        self.assertAlmostEqual(self.converter.convert(1, 'USD', 'EUR'), 0.93)

    def test_inverse_rate(self):
        self.converter.exchange_rates['EUR'] = 0.93
        self.assertAlmostEqual(self.converter.convert(1, 'EUR', 'USD'), 1 / 0.93)

    def test_unknown_currency(self):
        self.assertRaises(ValueError, self.converter.convert, 1, 'USD', '___')

    def test_unknown_currency2(self):
        self.assertRaises(ValueError, self.converter.convert, 1, '___', 'USD')

    def test_invalid_amount(self):
        self.assertRaises(ValueError, self.converter.convert, 'invalid', 'USD', 'EUR')

    def test_zero_amount(self):
        self.assertEqual(self.converter.convert(0, 'USD', 'EUR'), 0)

    def test_negative_amount(self):
        self.assertRaises(ValueError, self.converter.convert, -1, 'USD', 'EUR')

    @patch('main.requests.get')
    def test_api_success(self, mock_get):
        mock_get.return_value.json.return_value = {'EUR': {'rate': 0.93}}
        self.converter.update_exchange_rates()
        self.assertIn('EUR', self.converter.exchange_rates)

    @patch('main.requests.get')
    @patch('builtins.open', new_callable=mock_open, read_data='{"USD": 1}')
    def test_api_failure_with_backup_file(self, mock_file, mock_get):
        mock_get.side_effect = Exception('API failure')
        mock_file.side_effect = FileNotFoundError()
        self.converter.exchange_rates = {'USD': 1}
        self.converter.update_exchange_rates()
        self.assertEqual(self.converter.exchange_rates, {'USD': 1})

    @patch('builtins.open', new_callable=mock_open, read_data='{"USD": 1, "EUR": 0.93}')
    def test_load_exchange_rates_from_file(self, mock_file):
        self.converter.load_exchange_rates()
        self.assertIn('EUR', self.converter.exchange_rates)

    def test_file_writing(self):
        with patch('builtins.open', mock_open()) as mock_file:
            self.converter.exchange_rates = {'USD': 1, 'EUR': 0.93}
            self.converter.update_exchange_rates()  # This should write to the file
            mock_file.assert_called_with('exchange_rates.txt', 'w')

    def test_precision(self):
        self.converter.exchange_rates['CHF'] = 1.08777
        amount_converted = self.converter.convert(1.0001, 'USD', 'CHF')
        self.assertAlmostEqual(amount_converted, 1.088, places=3)

    def test_extreme_values(self):
        self.converter.exchange_rates['JPY'] = 110.5
        self.assertAlmostEqual(self.converter.convert(1000000000, 'USD', 'JPY'), 110500000000)