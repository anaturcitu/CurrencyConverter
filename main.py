import requests


class CurrencyConverter:
    def __init__(self):
        self.exchange_rates = {}
        self.update_exchange_rates()

    def update_exchange_rates(self):
        # URL-ul pentru ratele de schimb valutar pentru USD
        url = "https://www.floatrates.com/daily/usd.json"

        try:
            response = requests.get(url)
            rates = response.json()

            # actualizam ratele de schimb, se include si USD pentru simplitate
            self.exchange_rates = {'USD': 1}
            for code, data in rates.items():
                self.exchange_rates[code.upper()] = data['rate']

        except Exception as e:
            print(f"Eroare la actualizarea ratelor de schimb: {e}")

    def convert(self, amount, from_currency, to_currency):
        from_currency = from_currency.upper()
        to_currency = to_currency.upper()

        if from_currency not in self.exchange_rates:
            raise ValueError("Moneda initiala nu este suportata.")

        if to_currency not in self.exchange_rates:
            raise ValueError("Moneda finala nu este suportata.")

        # convertim suma în USD daca moneda sursa nu este USD
        if from_currency != 'USD':
            amount = amount / self.exchange_rates[from_currency]

        # convertim suma din USD în moneda destinatie
        return amount * self.exchange_rates[to_currency]


converter = CurrencyConverter()
try:
    amount_converted = converter.convert(100, 'USD', 'EUR')
    print(f"100 USD este echivalentul a {amount_converted} EUR.")
except ValueError as e:
    print(e)