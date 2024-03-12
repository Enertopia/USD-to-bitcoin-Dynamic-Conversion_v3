# Coded by Emiliano Solazzi Griminger 2023. Coinblend

import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Constants
CONVERSION_RATE = 0.000020  # Conversion rate: 1 fiat = 0.000020 BTC
MERCHANT_PRESETS = {1: 0.10, 2: 0.15, 3: 0.25, 4: 0.50, 5: 0.75, 6: 0.80}  # Preset conversion percentages

def simulate_server_conversion(amount_fiat, conversion_rate=CONVERSION_RATE):
    """
    Simulates the server-side conversion of fiat to Bitcoin.

    :param amount_fiat: The amount of fiat currency to convert.
    :param conversion_rate: The conversion rate for the specific transaction.
    :return: A dictionary with the conversion result.
    """
    bitcoin_amount = amount_fiat * conversion_rate
    return {
        'amount_fiat': amount_fiat,
        'bitcoin_amount': bitcoin_amount,
        'conversion_rate': conversion_rate
    }

def convert_to_bitcoin(amount_fiat, conversion_percentage):
    """
    Converts fiat currency to Bitcoin based on the merchant's conversion percentage.

    :param amount_fiat: The total amount of fiat currency.
    :param conversion_percentage: The merchant's chosen conversion percentage.
    """
    try:
        # Calculate the amount to be converted and the amount to keep in the bank account
        amount_to_convert = amount_fiat * conversion_percentage
        amount_to_keep = amount_fiat - amount_to_convert

        # Simulate server response for the conversion
        conversion_result = simulate_server_conversion(amount_to_convert)

        # Log conversion details
        logging.info(f"Total Fiat Amount: {amount_fiat}")
        logging.info(f"Amount to Bank Account: {amount_to_keep:.2f}")
        logging.info(f"Amount Converted to Bitcoin: {conversion_result['bitcoin_amount']:.8f} BTC")
        logging.info(f"Conversion Rate: {conversion_result['conversion_rate']} BTC per fiat unit")

    except Exception as e:
        logging.error(f"An error occurred during conversion: {e}")

def set_merchant_percentage():
    """
    Allows the merchant to set a conversion percentage from the preset options.

    :return: The chosen conversion percentage.
    """
    logging.info("Merchant Settings: Choose a preset conversion percentage:")
    for option, percentage in MERCHANT_PRESETS.items():
        logging.info(f"{option}. {percentage * 100}%")

    while True:
        choice = input("Enter the number corresponding to your choice: ")
        if choice.isdigit() and int(choice) in MERCHANT_PRESETS:
            return MERCHANT_PRESETS[int(choice)]
        else:
            logging.error("Invalid choice. Please enter a number corresponding to the options.")

def get_float_input(prompt):
    """
    Safely obtains a float input from the user.

    :param prompt: The prompt to display to the user.
    :return: The user input as a float.
    """
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            logging.error("Please enter a valid number.")

def main():
    logging.info("Starting the fiat to Bitcoin conversion client.")

    try:
        # Set the initial conversion percentage
        merchant_conversion_percentage = set_merchant_percentage()

        # Get the total fiat amount from the user
        fiat_amount = get_float_input("Enter the total fiat amount: ")

        # Convert to Bitcoin based on the chosen percentage
        convert_to_bitcoin(fiat_amount, merchant_conversion_percentage)

    except KeyboardInterrupt:
        logging.info("Conversion process interrupted by the user.")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")

if __name__ == '__main__':
    main()
