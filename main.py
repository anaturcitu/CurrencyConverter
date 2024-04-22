import requests
import tkinter as tk
from tkinter import ttk
import json


class CurrencyConverter:
    def __init__(self):
        self.exchange_rates = {}
        self.update_exchange_rates()


    def load_exchange_rates(self):
        try:
            # incarcam datele din fisierul text
            with open('exchange_rates.txt', 'r') as file:
                self.exchange_rates = json.load(file)
        except FileNotFoundError:
            print("Nu există un fișier cu ratele de schimb.")


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

            # Salvăm datele în fișierul text
            with open('exchange_rates.txt', 'w') as file:
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


class ConverterGUI:
    def __init__(self):
        self.converter = CurrencyConverter()

        self.window = tk.Tk()
        self.window.title("Convertor Valutar")
        self.window.geometry('300x200')

        self.main_frame = ttk.Frame(self.window, padding="10")
        self.main_frame.pack(expand=True, fill='both')

        ttk.Label(self.main_frame, text="Suma:").grid(column=0, row=0, sticky='w')
        self.amount_entry = ttk.Entry(self.main_frame)
        self.amount_entry.grid(column=1, row=0, sticky='ew', padx=5, pady=5)
        self.amount_entry.insert(0, "1")  # Setează valoarea implicită a sumei la 1

        ttk.Label(self.main_frame, text="Din moneda:").grid(column=0, row=1, sticky='w')
        self.from_currency_combo = ttk.Combobox(self.main_frame, values=list(self.converter.exchange_rates.keys()))
        self.from_currency_combo.grid(column=1, row=1, sticky='ew', padx=5, pady=5)
        self.from_currency_combo.current(0)

        ttk.Label(self.main_frame, text="In moneda:").grid(column=0, row=2, sticky='w')
        self.to_currency_combo = ttk.Combobox(self.main_frame, values=list(self.converter.exchange_rates.keys()))
        self.to_currency_combo.grid(column=1, row=2, sticky='ew', padx=5, pady=5)
        self.to_currency_combo.current(1)

        self.convert_button = ttk.Button(self.main_frame, text="Convert", command=self.perform_conversion)
        self.convert_button.grid(column=0, row=3, columnspan=2, sticky='ew', padx=5, pady=5)

        ttk.Label(self.main_frame, text="Rezultat:").grid(column=0, row=4, sticky='w')
        self.result_display = ttk.Label(self.main_frame, text="")
        self.result_display.grid(column=1, row=4, sticky='ew', padx=5, pady=5)

        self.main_frame.columnconfigure(1, weight=1)

        self.window.mainloop()

    def perform_conversion(self):
        amount = self.amount_entry.get()
        from_currency = self.from_currency_combo.get()
        to_currency = self.to_currency_combo.get()
        try:
            amount = float(amount)
            converted_amount = self.converter.convert(amount, from_currency, to_currency)
            self.result_display.config(text=f"{converted_amount:.2f}")
        except ValueError:
            self.result_display.config(text="Eroare la conversie")


if __name__ == '__main__':
    app = ConverterGUI()
