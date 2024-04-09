from ta.utils import dropna
from ta.volatility import BollingerBands
from ta.trend import ADXIndicator
from ta.volatility import AverageTrueRange
from ta.trend import SMAIndicator
from ta.momentum import RSIIndicator
from ta.volume import VolumeWeightedAveragePrice
from datetime import datetime as dt
import yfinance as yf
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from hurst import compute_Hc
from .signal_generator import fetch_candlestick_data
from configs.server_conf import logger
pd.options.mode.chained_assignment = None  # default='warn'
# init methond to construct and provide all thevariables that will be required by the strategy

# init methond to construct and provide all thevariables that will be required by the strategy
# start with single momentum strategy

# init methond to construct and provide all thevariables that will be required by the strategy

class Momentum_Hurst_RSI():

    def __init__(self, symbol, start, end, short_term_window, long_term_window, hurst_window, interval = '1d'):
        self.symbol = symbol
        self.start = start
        self.end = end
        self.ST_window = short_term_window
        self.LT_window = long_term_window
        # Hurst exponent
        self.hurst_window = hurst_window

        self.interval = interval

        # RSI indicator, same as the short term window
        self.RSI_window = short_term_window

        self.prepare_data()
    

    def prepare_data(self):

        stock_data = yf.Ticker(self.symbol)
        hist_stock = stock_data.history(start = self.start, end = self.end, interval = self.interval)

        bt_data = pd.DataFrame()
        bt_data['Close_Price'] = hist_stock['Close']

        # Calculate the momentum and the Hurst exponent
        bt_data['ShortTermMomentum'] = bt_data['Close_Price'] - bt_data['Close_Price'].shift(self.ST_window)
        bt_data['LongTermMomentum'] = bt_data['Close_Price'] - bt_data['Close_Price'].shift(self.LT_window)    
        bt_data['Hurst'] = bt_data['Close_Price'].rolling(window=self.hurst_window).apply(lambda x: compute_Hc(x)[0])

        # Calculating the RSI
        rsi_indicator = RSIIndicator(close = hist_stock["Close"], window = self.RSI_window, fillna = False)
        RSI = rsi_indicator.rsi()

        # Adding the RSI to the dataframe
        bt_data['RSI'] = RSI

        bt_data = bt_data.dropna()
        self.data = bt_data
    
    def stratrgy(self):
        data = self.data
         
        # data['Position'] = 1
        data.loc[(data['Hurst'] > 0.5) & (data['ShortTermMomentum'] > 0) & (data['LongTermMomentum'] > 0), 'Position'] = 1 # Hurst exponent greater than 0.5, short term and long term momentum greater than 0, buy
        data.loc[(data['Hurst'] > 0.5) & (data['ShortTermMomentum'] < 0) & (data['LongTermMomentum'] < 0), 'Position'] = -1

        # Out of the market
        data.loc[(data['RSI'] <= 70) & (data['Hurst'] > 0.5) & ((data['ShortTermMomentum'] > 0) & (data['LongTermMomentum'] < 0) | (data['ShortTermMomentum'] < 0) & (data['LongTermMomentum'] > 0)), 'Position'] = 1
        data.loc[(data['RSI'] > 70) & (data['Hurst'] > 0.5) & ((data['ShortTermMomentum'] > 0) & (data['LongTermMomentum'] < 0) | (data['ShortTermMomentum'] < 0) & (data['LongTermMomentum'] > 0)), 'Position'] = -1
        data.loc[(data['Hurst'] < 0.5) & (data['RSI'] <= 70), 'Position'] = 1
        data.loc[(data['Hurst'] < 0.5) & (data['RSI'] > 70), 'Position'] = -1

        data['Signal'] = data['Position'].diff()
        data = data.dropna()

        data['Stock_Returns'] = np.log(data['Close_Price']/data['Close_Price'].shift(1))
        data['Strategy_Returns'] = data['Stock_Returns'] * data['Position'].shift(1)

        self.visualise_data = data
    
    def visualise_strategy(self):
        logger.info('-------------------')
        logger.info('Visualising the Strategy crossover period')
        bt_data = self.visualise_data
        plt.figure(figsize=(15, 5))
        plt.plot(bt_data["Close_Price"] ,color='black', label='Price', linestyle='dashed')
        plt.plot(bt_data["ShortTermMomentum"], color='b', label='Short term Momentum')
        plt.plot(bt_data["LongTermMomentum"], color='r', label='Long term Momentum')
        plt.plot(bt_data["Hurst"], color='g', label='Hurst Exponent')

        # plot ‘buy crossover’ signals.
        # Because I have used +1 and -1,
        # A buy signal will be created when the position was -1 and it turned to +1
        # difference of +1 - -1 will give me 2

        plt.plot(bt_data[bt_data['Signal'] == 2].index,
                bt_data['Close_Price'][bt_data['Signal'] == 2],
                '^', markersize = 15, color = 'g', label = 'buy/long')

        # plot ‘sell crossover ’ signals
        plt.plot(bt_data[bt_data['Signal'] == -2].index,
                bt_data['Close_Price'][bt_data['Signal'] == -2],
                'v', markersize = 15, color = 'r', label = 'sell/short')

        plt.xlabel("Days")
        plt.ylabel("Price")
        plt.title(f"Moving Averages Crossover {self.ST_window} Vs {self.LT_window}")
        plt.legend()
        plt.grid()
        plt.show()

    def performance(self):

        logger.info('-------------------')
        logger.info('Performance of the Strategy')
        logger.info('-------------------')

        bt_data = self.visualise_data

        daily_ret = bt_data[['Stock_Returns', 'Strategy_Returns']].mean()
        annual_ret = daily_ret * 252
        annual_regular_ret = np.exp(annual_ret) - 1

        logger.info('Annual Regular Return:', annual_regular_ret)

        daily_std = bt_data[['Stock_Returns', 'Strategy_Returns']].std()
        annual_std = daily_std * math.sqrt(252)
        daily_regular_std = (np.exp(bt_data[['Stock_Returns', 'Strategy_Returns']]) - 1).std()
        annual_regular_std = daily_regular_std * math.sqrt(252)

        logger.info('Annual Regular Standard Deviation:', annual_regular_std)

        sr = annual_regular_ret / annual_regular_std

        logger.info('Sharpe Ratio:', sr)

    def returns_plot(self):
        bt_data = self.visualise_data
        title = f'Returns plot for Momentum with Hurst Strategy for {self.ST_window} Vs {self.LT_window}'
        bt_data[['Stock_Returns', 'Strategy_Returns']].cumsum().plot(title = title, figsize=(15, 6))
        plt.show()

    def drawdown(self):
        bt_data = self.visualise_data
        bt_data['Gross_Cum_Returns'] = bt_data['Strategy_Returns'].cumsum().apply(np.exp)
        bt_data['Cum_Max'] = bt_data['Gross_Cum_Returns'].cummax()

        title = f'Drawdown for Momentum with Hurst Strategy for {self.ST_window} Vs {self.LT_window}'
        bt_data[['Gross_Cum_Returns', 'Cum_Max']].dropna().plot(title = title, figsize=(15, 6))

        drawdown = bt_data['Cum_Max'] - bt_data['Gross_Cum_Returns']

        logger.info('The Maximum Drawdown is:', drawdown.max())
        logger.info('-'*20)

        zero_periods = drawdown[drawdown == 0]
        delta_values = zero_periods.index[1:] - zero_periods.index[:-1]
        logger.info('The Longest Drawdown period is:', delta_values.max())
# Function to calculate annual return, annual standard deviation and Sharpe ratio for multiple stocks
def calculate_metrics(data, prefix):
    daily_ret = data.mean(axis=0)
    annual_ret = daily_ret * 252
    annual_regular_ret = np.exp(annual_ret) - 1

    daily_std = data.std()
    annual_std = daily_std * math.sqrt(252)
    daily_regular_std = (np.exp(data) - 1).std()
    annual_regular_std = daily_regular_std * math.sqrt(252)

    sr = annual_regular_ret / annual_regular_std
    logger.info(f"Annual Return ({prefix}):", annual_ret, annual_regular_ret)
    logger.info(f'Annual Std ({prefix}):', annual_std, annual_regular_std)
    logger.info(f'Annual Regular Return ({prefix}):', annual_regular_ret)
    logger.info(f'Annual Regular Standard Deviation ({prefix}):', annual_regular_std)
    logger.info(f'Sharpe Ratio ({prefix}):', sr)
    return pd.DataFrame({'Name':prefix,'Annual Return': annual_regular_ret, 'Annual Std': annual_regular_std, 'Sharpe Ratio': sr}, index=[prefix])


# Add drawdown analysis to the function
def run_strategy_and_analyze(stocks, start_date, end_date, short_window, long_window, hurst_window):
    results = pd.DataFrame()
    metrics = pd.DataFrame()
    trades = pd.DataFrame()
    for stock in stocks:
        logger.info('-------------------')
        logger.info('Running the Strategy for:', stock)
        logger.info('-------------------')
        momentum_hurst_rsi = Momentum_Hurst_RSI(stock, start_date, end_date, short_window, long_window, hurst_window)
        momentum_hurst_rsi.stratrgy()
        #momentum_hurst_rsi.data.to_csv(stock + '_data.csv')
        # add to trades if signal is 2 or -2
        records = momentum_hurst_rsi.data[momentum_hurst_rsi.data['Signal'] != 0]
        records['Stock'] = stock
        trades = pd.concat([trades, records])
        results['stock_returns_'+ stock] = momentum_hurst_rsi.visualise_data['Stock_Returns']
        metrics = pd.concat([metrics, calculate_metrics(momentum_hurst_rsi.visualise_data['Stock_Returns'], stock)])
        results['strategy_returns_'+ stock] = momentum_hurst_rsi.visualise_data['Strategy_Returns']
        metrics = pd.concat([metrics, calculate_metrics(momentum_hurst_rsi.visualise_data['Strategy_Returns'], stock + ' Strategy')])
    # sort trades by Date
    #trades = trades.sort_index()
    #trades.to_csv('trades.csv')

    stock_returns = results.filter(like='stock')
    strategy_returns = results.filter(like='strategy')

    results['portfolio_returns'] = stock_returns.sum(axis=1) / len(stocks)
    results['portfolio_strategy'] = strategy_returns.sum(axis=1) / len(stocks)

    plot_title = 'Portfolio Returns for the stocks'
    columns_to_plot = ['portfolio_returns', 'portfolio_strategy'] + ['stock_returns_' + stock for stock in stocks]
    #results[columns_to_plot].cumsum().plot(title=plot_title, figsize=(15, 6))

    metrics = pd.concat([metrics, calculate_metrics(results['portfolio_returns'], 'Portfolio Returns')])
    metrics = pd.concat([metrics, calculate_metrics(results['portfolio_strategy'], 'Portfolio Strategy')])

    # Calculate and plot drawdown
    results['cumulative_portfolio_strategy'] = results['portfolio_strategy'].cumsum()
    results['cum_max'] = results['cumulative_portfolio_strategy'].cummax()

    title = 'Drawdown for Momentum with Hurst and RSI Strategy'
    results[['cumulative_portfolio_strategy', 'cum_max']].dropna().plot(title = title, figsize=(15, 6))
    
    drawdown = results['cum_max'] - results['cumulative_portfolio_strategy']

    logger.info('The Maximum Drawdown is:', drawdown.max())
    zero_periods = drawdown[drawdown == 0]
    delta_values = zero_periods.index[1:] - zero_periods.index[:-1]
    logger.info('The Longest Drawdown period is:', delta_values.max())
    # to csv, if exists, rewrite
    results.to_csv('results.csv',)
    metrics.to_csv('metrics.csv')
    trades.to_csv('trades.csv')
    trades.sort_index(inplace=True, ascending=False)
    trades = trades.reset_index().rename({'index': 'Date'}, axis=1)
    trades_df = trades[["Date", "Stock", "Signal", "Close_Price"]]
    # make date in DD/MM/YY by regex but not dt
    trades_df["Date"] = trades_df["Date"].apply(lambda x: x.strftime("%d/%m/%y"))
    # make signal to Buy/Sell
    trades_df["Signal"] = trades_df["Signal"].apply(lambda x: "Buy" if x == 2 else "Sell")
    # make close price to 2 decimal places
    trades_df["Close_Price"] = trades_df["Close_Price"].round(2)
    trades_df.rename(columns={"Close_Price": "Close", "Signal":"Action"}, inplace=True)
    trades_df.to_csv("mini_trades.csv", index=False)
    return results, metrics

def run_strategy(stocks=['AAPL', 'GOOGL', 'NFLX', 'AMZN', 'META'], start_date='2015-01-01', end_date='2019-12-31', short_window=5, long_window=21, hurst_window=200):
    results = pd.read_csv('results.csv', index_col=0)
    metrics = pd.read_csv('metrics.csv', index_col=0)
    trades = pd.read_csv('mini_trades.csv', index_col=0)
    trades = trades.reset_index().rename({'index': 'Date'}, axis=1)
    # make trades in this order: ['Date', 'Stock','Close', 'Action']
    trades = trades[["Date", "Stock", "Close", "Action"]]
    results = results.reset_index().rename({'index': 'Date'}, axis=1)
    results['cumulative_portfolio_strategy'] = results['portfolio_strategy'].cumsum()
    results['cumulative_portfolio_returns'] = results['portfolio_returns'].cumsum()
    results['Date'] = pd.to_datetime(results['Date'])
    full_trades = pd.read_csv("trades.csv")
    # reverse the order of full trades
    return results, metrics, trades,full_trades
    
    stocks = ['AAPL', 'GOOGL', 'NFLX', 'AMZN', 'META']
    start_date = '2015-01-01'
    end_date = '2019-12-31'
    short_window = 5
    long_window = 21
    hurst_window = 200
    
    return run_strategy_and_analyze(stocks, start_date, end_date, short_window, long_window, hurst_window)


def fetch_data(instrument_name, lookback_count, granularity='S5', price='M'):
    resp = fetch_candlestick_data(instrument_name, lookback_count, granularity, price)['candles']
    # resp = list[{'complete': True, 'volume': 2, 'time': '', 'mid': {'o': '', 'h': '', 'l': '', 'c': ''}}]
    # convert to list[{'time':'', open:'', high:'', low:'', close:''}]
    resp = [{'time': x['time'], 'open': x['mid']['o'], 'high': x['mid']['h'], 'low': x['mid']['l'], 'close': x['mid']['c']} for x in resp]
    # convert '2024-04-08T11:30:50.000000000Z' kind of format into UTC time (int)
    resp = [{'time': int(dt.strptime(x['time'], '%Y-%m-%dT%H:%M:%S.%f000Z').timestamp()), 'open': x['open'], 'high': x['high'], 'low': x['low'], 'close': x['close']} for x in resp]
    return resp
if __name__ == '__main__':
    stocks = ['AAPL', 'GOOGL', 'NFLX', 'AMZN', 'META']
    start_date = '2015-01-01'
    end_date = '2019-12-31'
    short_window = 5
    long_window = 21
    hurst_window = 200
    run_strategy_and_analyze(stocks, start_date, end_date, short_window, long_window, hurst_window)