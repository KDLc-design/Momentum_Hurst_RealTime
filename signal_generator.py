import numpy as np
from oandapyV20 import API
# API processes requests that can be created from the endpoints
from oandapyV20.endpoints.instruments import InstrumentsCandles
from hurst import compute_Hc

access_token = "9c7349b9a9bd3d17409758cb7e29e53f-7fcbdfe7bc0636788aa51f7e4a95601f"
account_id = "101-003-28600525-001"

accountID = account_id
access_token = access_token


def fetch_candlestick_data(instrument_name, lookback_count):
    # Initialize the Oanda API client
    api = API(access_token=access_token, environment="practice")

    # Define the parameters for the candlestick data request
    params = {
        'count': lookback_count,
        'granularity': 'H1',
        'price': 'M',  # Midpoint candlestick prices
    }

    # Request the candlestick data from Oanda API
    candles_request = InstrumentsCandles(instrument=instrument_name, params=params)
    response = api.request(candles_request)

    # Extract the close prices from the response
    close_prices = [float(candle['mid']['c']) for candle in response['candles']]

    return close_prices


def calculate_hurst_exponent(close_prices, hurst_period):
    # Calculate the Hurst exponent
    relevant_close_prices = close_prices[-hurst_period:]
    hurst, _, _ = compute_Hc(relevant_close_prices)
    return hurst


def calculate_momentum(close_prices, period):
    # Calculate the momentum
    momentum = close_prices[-1] - close_prices[-period]
    return momentum


def calculate_rsi(close_prices, period):
    # Calculate the RSI
    delta = np.diff(close_prices)
    gain = delta[delta > 0]
    loss = -delta[delta < 0]

    avg_gain = np.mean(gain[:period])
    avg_loss = np.mean(loss[:period])

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    return rsi


def generate_signal(instrument_name, lookback_count, st_period, lt_period, hurst_period):
    # Fetch candlestick data
    close_prices = fetch_candlestick_data(instrument_name, lookback_count)

    # Calculate Hurst exponent
    hurst = calculate_hurst_exponent(close_prices, hurst_period)
    print("Hurst Exponent:", hurst)

    # Calculate short-term Momentum
    short_term_momentum = calculate_momentum(close_prices, st_period)
    print("Short-term Momentum:", short_term_momentum)

    # Calculate long-term Momentum
    long_term_momentum = calculate_momentum(close_prices, lt_period)
    print("Long-term Momentum:", long_term_momentum)

    # Calculate RSI
    rsi = calculate_rsi(close_prices, st_period)
    print("RSI:", rsi)

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
