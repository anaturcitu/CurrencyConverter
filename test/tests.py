import unittest
import json
from unittest.mock import patch, mock_open
from src.main import CurrencyConverter

class TestCurrencyConverter(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Initialize the CurrencyConverter instance
        cls.converter = CurrencyConverter()

    def test_same_currency(cls):
        cls.assertEqual(cls.converter.convert(1, 'USD', 'USD'), 1)

    def test_different_rate(cls):
        cls.converter.exchange_rates['EUR'] = 0.93
        cls.assertAlmostEqual(cls.converter.convert(1, 'USD', 'EUR'), 0.93)

    def test_inverse_rate(cls):
        cls.converter.exchange_rates['EUR'] = 0.93
        cls.assertAlmostEqual(cls.converter.convert(1, 'EUR', 'USD'), 1 / 0.93)

    def test_unknown_currency(cls):
        cls.assertRaises(ValueError, cls.converter.convert, 1, 'USD', '___')

    def test_unknown_currency2(cls):
        cls.assertRaises(ValueError, cls.converter.convert, 1, '___', 'USD')

    def test_invalid_amount(cls):
        cls.assertRaises(ValueError, cls.converter.convert, 'invalid', 'USD', 'EUR')

    def test_zero_amount(cls):
        cls.assertEqual(cls.converter.convert(0, 'USD', 'EUR'), 0)

    def test_negative_amount(cls):
        cls.assertRaises(ValueError, cls.converter.convert, -1, 'USD', 'EUR')

    @patch('src.main.requests.get')
    def test_api_success(cls, mock_get):
        mock_get.return_value.json.return_value = {'EUR': {'rate': 0.93}}
        cls.converter.update_exchange_rates()
        cls.assertIn('EUR', cls.converter.exchange_rates)

    @patch('src.main.requests.get')
    @patch('builtins.open', new_callable=mock_open, read_data='{"USD": 1}')
    def test_api_failure_with_backup_file(cls, mock_file, mock_get):
        mock_get.side_effect = Exception('API failure')
        mock_file.side_effect = FileNotFoundError()
        cls.converter.exchange_rates = {'USD': 1}
        cls.converter.update_exchange_rates()
        cls.assertEqual(cls.converter.exchange_rates, {'USD': 1})

    @patch('builtins.open', new_callable=mock_open, read_data='{"USD": 1, "EUR": 0.93}')
    def test_load_exchange_rates_from_file(cls, mock_file):
        cls.converter.load_exchange_rates()
        cls.assertIn('EUR', cls.converter.exchange_rates)

    def test_file_writing(cls):
        with patch('builtins.open', mock_open()) as mock_file:
            cls.converter.exchange_rates = {'USD': 1, 'EUR': 0.93}
            cls.converter.update_exchange_rates()  # This should write to the file
            mock_file.assert_called_with('../exchange_rates.txt', 'w')

    def test_precision(cls):
        cls.converter.exchange_rates['CHF'] = 1.08777
        amount_converted = cls.converter.convert(1.0001, 'USD', 'CHF')
        cls.assertAlmostEqual(amount_converted, 1.088, places=3)

    def test_extreme_values(cls):
        cls.converter.exchange_rates['JPY'] = 110.5
        cls.assertAlmostEqual(cls.converter.convert(1000000000, 'USD', 'JPY'), 110500000000)