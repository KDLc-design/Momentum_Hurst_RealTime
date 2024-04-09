import numpy as np
from oandapyV20.exceptions import V20Error
# API processes requests that can be created from the endpoints
from oandapyV20.endpoints.instruments import InstrumentsCandles
from hurst import compute_Hc

from configs.oanda_conf import CLIENT_CONFIG
from configs.server_conf import logger

def fetch_candlestick_data(instrument_name, lookback_count, granularity='S5', price='M'):
    # Initialize the Oanda API client

    # Define the parameters for the candlestick data request
    params = {
        'count': lookback_count,
        'granularity': granularity,
        'price': price,  # Midpoint candlestick prices
    }

    # Request the candlestick data from Oanda API
    candles_request = InstrumentsCandles(instrument=instrument_name, params=params)
    # ensure that the request is successful
    while True:
        try:
            return CLIENT_CONFIG.client_api.request(candles_request)
        except V20Error as e:
            logger.info(f"V20Error occurred: {e}")
        except Exception as e:
            logger.info(f"Exception occurred: {e}")

def calculate_hurst_exponent(close_prices, hurst_period):
    # Calculate the Hurst exponent
    relevant_close_prices = close_prices[-hurst_period:]
    hurst, _, _ = compute_Hc(relevant_close_prices)
    return hurst


def calculate_momentum(close_prices, period):
    # Calculate the momentum
    return close_prices[-1] - close_prices[-period]



def calculate_rsi(close_prices, period):
    # Calculate the RSI
    delta = np.diff(close_prices)
    gain = delta[delta > 0]
    loss = -delta[delta < 0]

    avg_gain = np.mean(gain[:period])
    avg_loss = np.mean(loss[:period])

    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))


def generate_signal(instrument_name, lookback_count, st_period, lt_period, hurst_period):
    # Fetch candlestick data
    response = fetch_candlestick_data(instrument_name, lookback_count)
    close_prices = [float(candle['mid']['c']) for candle in response['candles']]
    # Calculate Hurst exponent
    hurst = calculate_hurst_exponent(close_prices, hurst_period)
    logger.info(f"Hurst Exponent: {hurst:.6f}")

    # Calculate short-term Momentum
    short_term_momentum = calculate_momentum(close_prices, st_period)
    logger.info(f"Short-term Momentum:{short_term_momentum:.6f}")

    # Calculate long-term Momentum
    long_term_momentum = calculate_momentum(close_prices, lt_period)
    logger.info(f"Long-term Momentum: {long_term_momentum:.6f}")

    # Calculate RSI
    rsi = calculate_rsi(close_prices, st_period)
    logger.info(f"RSI: {rsi:.6f}")

    # Check for crossover
    if hurst > 0.8 and short_term_momentum > 0 and long_term_momentum > 0:
        signal = "BUY"
    elif hurst < 0.2 and short_term_momentum < 0 and long_term_momentum < 0:
        signal = "BUY"
    elif hurst > 0.8 and short_term_momentum < 0 and long_term_momentum < 0:
        signal = "SELL"
    elif hurst < 0.2 and short_term_momentum > 0 and long_term_momentum > 0:
        signal = "SELL"
    elif 0.8 >= hurst >= 0.2 and rsi > 70:
        signal = "SELL"
    elif 0.8 >= hurst >= 0.2 and rsi <= 30:
        signal = "BUY"
    else:
        signal = "HOLD"

    return signal
#generate_signal("EUR_USD", 200, 5, 20, 100)