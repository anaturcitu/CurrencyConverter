import requests
import json


class CurrencyConverter:
    def __init__(self):
        self.exchange_rates = {}
        self.update_exchange_rates()

    def load_exchange_rates(self):
        try:
            # incarcam datele din fisierul text
            with open('../exchange_rates.txt', 'r') as file:
                self.exchange_rates = json.load(file)
        except FileNotFoundError:
            print("Nu exista un fisier cu ratele de schimb.")

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

            # Salvam datele in fisierul text
            with open('../exchange_rates.txt', 'w') as file:
                json.dump(self.exchange_rates, file)

        except Exception as e:
            print(f"Eroare la actualizarea ratelor de schimb: {e}")
            self.load_exchange_rates()

    def convert(self, amount, from_currency, to_currency):
        from_currency = from_currency.upper()
        to_currency = to_currency.upper()

        if not isinstance(amount, (int, float)):
            raise ValueError("Valoarea trebuie sa fie in tip numerar.")

        if amount < 0:
            raise ValueError("Valoarea trebuie sa fie pozitiva.")

        if from_currency not in self.exchange_rates:
            raise ValueError("Moneda initiala nu este suportata.")

        if to_currency not in self.exchange_rates:
            raise ValueError("Moneda finala nu este suportata.")

        # convertim suma în USD daca moneda sursa nu este USD
        if from_currency != 'USD':
            amount = amount / self.exchange_rates[from_currency]

        # convertim suma din USD în moneda destinatie
        return amount * self.exchange_rates[to_currency]
