# Coded by Emiliano Solazzi Griminger, 2023. Coinblend
# Enhancements include real-time conversion rates, a GUI, database support for history and preferences, and advanced logging.

import logging
import requests
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

# Configure logging
logging.basicConfig(filename='conversion_app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize database
def initialize_db():
    conn = sqlite3.connect('conversion_history.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS history
                 (date TEXT, fiat_amount REAL, conversion_percentage REAL, bitcoin_amount REAL)''')
    c.execute('''CREATE TABLE IF NOT EXISTS preferences
                 (key TEXT PRIMARY KEY, value TEXT)''')
    conn.commit()
    conn.close()

# Fetch real-time conversion rate from an external API
def get_real_time_conversion_rate():
    try:
        response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd')
        data = response.json()
        return data['bitcoin']['usd']
    except requests.RequestException as e:
        logging.error(f"Error fetching conversion rate: {e}")
        messagebox.showerror("Error", "Failed to fetch conversion rate. Check your internet connection.")
        return None

# Save conversion to database
def save_conversion(fiat_amount, conversion_percentage, bitcoin_amount):
    conn = sqlite3.connect('conversion_history.db')
    c = conn.cursor()
    c.execute("INSERT INTO history VALUES (?, ?, ?, ?)", (datetime.now().isoformat(), fiat_amount, conversion_percentage, bitcoin_amount))
    conn.commit()
    conn.close()

# Perform conversion and log the results
def convert_and_log(amount_fiat, conversion_percentage):
    conversion_rate = get_real_time_conversion_rate()
    if conversion_rate is not None:
        bitcoin_amount = (amount_fiat * conversion_percentage) / conversion_rate
        save_conversion(amount_fiat, conversion_percentage, bitcoin_amount)
        logging.info(f"Conversion successful: {amount_fiat} fiat to {bitcoin_amount:.8f} BTC")
        return bitcoin_amount
    else:
        return None

# GUI for application
def create_gui():
    window = tk.Tk()
    window.title("Fiat to Bitcoin Converter")

    ttk.Label(window, text="Amount in Fiat:").grid(column=0, row=0, sticky=tk.W)
    amount_entry = ttk.Entry(window)
    amount_entry.grid(column=1, row=0, sticky=tk.EW)

    ttk.Label(window, text="Conversion Percentage:").grid(column=0, row=1, sticky=tk.W)
    percentage_entry = ttk.Entry(window)
    percentage_entry.grid(column=1, row=1, sticky=tk.EW)

    def on_convert():
        try:
            amount_fiat = float(amount_entry.get())
            conversion_percentage = float(percentage_entry.get()) / 100.0
            bitcoin_amount = convert_and_log(amount_fiat, conversion_percentage)
            if bitcoin_amount is not None:
                messagebox.showinfo("Conversion Result", f"Bitcoin Amount: {bitcoin_amount:.8f} BTC")
            else:
                messagebox.showerror("Error", "Conversion failed. Please try again later.")
        except ValueError as e:
            logging.error(f"Input error: {e}")
            messagebox.showerror("Error", "Invalid input. Please enter valid numbers.")

    ttk.Button(window, text="Convert", command=on_convert).grid(column=1, row=2, sticky=tk.W)

    window.mainloop()

if __name__ == '__main__':
    initialize_db()
    create_gui()
