from src.main import CurrencyConverter
import tkinter as tk
from tkinter import ttk


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
