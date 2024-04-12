import numpy as np
from oandapyV20.exceptions import V20Error
# API processes requests that can be created from the endpoints
from oandapyV20.endpoints.instruments import InstrumentsCandles
from hurst import compute_Hc
import os
import sys
# set to root path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from configs.oanda_conf import CLIENT_CONFIG, TRADE_CONFIG
from configs.server_conf import logger
from datetime import datetime as dt, timezone
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

def calculate_all_indicators(instrument_name, lookback_count, st_period, lt_period, hurst_period, close_prices=None):# Fetch candlestick data
    # if not none, fetch
    if instrument_name is not None:
        response = fetch_candlestick_data(instrument_name, lookback_count)
        close_prices = [float(candle['mid']['c']) for candle in response['candles']]
    hurst = calculate_hurst_exponent(close_prices, hurst_period)
    short_term_momentum = calculate_momentum(close_prices, st_period)
    long_term_momentum = calculate_momentum(close_prices, lt_period)
    rsi = calculate_rsi(close_prices, st_period)
    return hurst, short_term_momentum, long_term_momentum, rsi
def generate_signal(instrument_name, lookback_count, st_period, lt_period, hurst_period):
    hurst, short_term_momentum, long_term_momentum, rsi = calculate_all_indicators(instrument_name, lookback_count, st_period, lt_period, hurst_period)
    
    logger.info(f"Hurst Exponent: {hurst:.6f}")

    logger.info(f"Short-term Momentum:{short_term_momentum:.6f}")

    logger.info(f"Long-term Momentum: {long_term_momentum:.6f}")

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
def fetch_data(instrument_name, lookback_count, granularity='S5', price='M', include_indicators=False):
    resp = fetch_candlestick_data(instrument_name, lookback_count, granularity, price)['candles']
    # resp = list[{'complete': True, 'volume': 2, 'time': '', 'mid': {'o': '', 'h': '', 'l': '', 'c': ''}}]
    # convert to list[{'time':'', open:'', high:'', low:'', close:''}]
    resp = [{'time': x['time'], 'open': x['mid']['o'], 'high': x['mid']['h'], 'low': x['mid']['l'], 'close': x['mid']['c']} for x in resp]
    # convert '2024-04-08T11:30:50.000000000Z' kind of format into UTC time (note that we are singapore timezone)
    def convert_time(time):
        return dt.strptime(time, '%Y-%m-%dT%H:%M:%S.%f000Z').replace(tzinfo=timezone.utc).timestamp()
    candlestick_data = [{'time':convert_time(x['time']), 'open': x['open'], 'high': x['high'], 'low': x['low'], 'close': x['close']} for x in resp]
    if include_indicators:
        indicators = calculate_all_indicators(None,None,TRADE_CONFIG.st_period,TRADE_CONFIG.lt_period,TRADE_CONFIG.hurst_period,[float(x['close']) for x in candlestick_data])
        return candlestick_data, indicators
    return candlestick_data
if __name__ == "__main__":
    print(fetch_candlestick_data("EUR_USD", 200))