import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Simulated server-side conversion logic
CONVERSION_RATE = 0.000020  # Example conversion rate: 1 fiat = 0.000020 BTC

# Default percentage to be converted to Bitcoin
DEFAULT_PERCENTAGE = 0.05

# Merchant's preset conversion percentage (initially set to the default)
merchant_conversion_percentage = DEFAULT_PERCENTAGE

MERCHANT_PRESETS = [0.10, 0.15, 0.25, 0.50, 0.75, 0.80]

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

def convert_to_bitcoin(amount_fiat):
    """
    Converts a portion of the fiat currency amount to Bitcoin using a simulated server response.

    :param amount_fiat: The total amount of fiat currency.
    """
    global merchant_conversion_percentage  # Access the global variable

    try:
        # Calculate the amount to be converted based on the stored percentage
        amount_to_convert = amount_fiat * merchant_conversion_percentage

        # Calculate the amount to be kept in the bank account
        amount_to_keep = amount_fiat - amount_to_convert

        # Simulate server response for the conversion
        result = simulate_server_conversion(amount_to_convert)

        logging.info(f"Total Fiat Amount: {amount_fiat}")
        logging.info(f"Amount to Bank Account: {amount_to_keep:.2f}")
        logging.info(f"Amount Converted to Bitcoin: {result['bitcoin_amount']:.8f} BTC")
        logging.info(f"Conversion Rate: {result['conversion_rate']} BTC per fiat unit")

        # In a real scenario, you would proceed to send the converted Bitcoin to the merchant's wallet.
    except Exception as e:
        logging.error(f"An error occurred during conversion: {e}")

def get_float_input(prompt):
    """
    Safely obtains a float input from the user.

    :param prompt: The prompt to display to the user.
    :return: The user input as a float.
    """
    while True:
        try:
            user_input = input(prompt)
            return float(user_input)
        except ValueError:
            logging.error("Please enter a valid number.")

def set_merchant_percentage():
    """
    Allows the merchant to set a conversion percentage from the preset options.

    :return: The chosen conversion percentage.
    """
    global merchant_conversion_percentage  # Access the global variable

    logging.info("Merchant Settings: Choose a preset conversion percentage:")
    for i, percentage in enumerate(MERCHANT_PRESETS, 1):
        logging.info(f"{i}. {percentage * 100}%")

    choice = get_float_input("Enter the number corresponding to your choice: ")
    if 1 <= choice <= len(MERCHANT_PRESETS):
        merchant_conversion_percentage = MERCHANT_PRESETS[int(choice) - 1]
        logging.info(f"Conversion percentage set to {merchant_conversion_percentage * 100}%")
    else:
        logging.error("Invalid choice. Using the default percentage.")

def main():
    global merchant_conversion_percentage  # Access the global variable

    logging.info("Starting the fiat to Bitcoin conversion client.")

    # Set the initial conversion percentage (optional, can be done in a separate setting)
    set_merchant_percentage()

    # Get the total fiat amount from the user
    fiat_amount = get_float_input("Enter the total fiat amount: ")

    # Convert to Bitcoin based on the stored percentage
    convert_to_bitcoin(fiat_amount)

if __name__ == '__main__':
    main()
