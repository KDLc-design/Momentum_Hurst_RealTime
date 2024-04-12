import oandapyV20.endpoints.positions as positions
import oandapyV20.endpoints.orders as orders
import oandapyV20.endpoints.trades as trades
import oandapyV20.endpoints.pricing as pricing
from oandapyV20.endpoints import transactions
import time
import numpy as np
import pandas as pd
from dateutil.parser import isoparse
from oandapyV20.endpoints.accounts import AccountDetails
from oandapyV20.exceptions import V20Error
# from notification import send_email_notification
# set os env path
import os
import sys
# set to root path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from configs.oanda_conf import CLIENT_CONFIG, TRADE_CONFIG
from configs.server_conf import logger


def get_current_price(instrument):
    params = {
        "instruments": instrument
    }
    request = pricing.PricingInfo(accountID=CLIENT_CONFIG.account_id, params=params)
    response = CLIENT_CONFIG.client_api.request(request)

    if 'prices' in response and response['prices']:
        return float(response['prices'][0]['bids'][0]['price'])

    return None


def get_instrument_precision(instrument):
    instrument_precision = {
        "EUR_USD": 4,
        "AUD_USD": 4,
        "NZD_USD": 4,
        "GBP_USD": 4,
        "GBP_JPY": 2,
        "USD_JPY": 2,
        "EUR_JPY": 2
        }
    return instrument_precision.get(instrument)  # Set a default precision value if instrument not found


def get_current_balance():
    request = AccountDetails(accountID=CLIENT_CONFIG.account_id)
    response = CLIENT_CONFIG.client_api.request(request)

    if response and 'account' in response:
        account_info = response['account']
        balance = float(account_info['balance'])
        return balance

    return None


def get_quantity(instrument, trade_direction):
    current_price = get_current_price(instrument)
    take_profit_percentage = 0.02
    stop_loss_percentage = 0.02

    if trade_direction == "BUY":
        take_profit_price = round(current_price * (1 + take_profit_percentage), get_instrument_precision(instrument))
        stop_loss_price = round(current_price * (1 - stop_loss_percentage), get_instrument_precision(instrument))
    elif trade_direction == "SELL":
        take_profit_price = round(current_price * (1 - take_profit_percentage), get_instrument_precision(instrument))
        stop_loss_price = round(current_price * (1 + stop_loss_percentage), get_instrument_precision(instrument))
    else:
        logger.info("Invalid trade direction")
        return
    # logger.info(stop_loss_price, take_profit_price)

    trade_currency_2 = instrument[4:]
    position_size = None
    # A more complex calculation can be done 

    if "USD" in trade_currency_2:
        position_size = 100000
    elif "JPY" in trade_currency_2:
        position_size = 50000
    else:
        logger.info("Unsupported currency in the denominator")
        position_size = None
    
    if trade_direction == "BUY":
        position_size = position_size 
    else:
        position_size = -position_size

    return stop_loss_price, take_profit_price, position_size


def get_open_positions():
    request = positions.OpenPositions(accountID=CLIENT_CONFIG.account_id)
    response = CLIENT_CONFIG.client_api.request(request)
    open_positions = response.get("positions", [])
    return open_positions
def get_filled_orders():
    from oandapyV20.endpoints import orders
    import pandas as pd
    request = orders.OrderList(accountID=CLIENT_CONFIG.account_id,params={'instrument': 'EUR_USD', 'state': 'FILLED','count':10})

    return CLIENT_CONFIG.client_api.request(request)['orders']
    
def get_transaction_stream():
    from oandapyV20.endpoints import transactions
    import pandas as pd
    import time
    request = transactions.TransactionsStream(accountID=CLIENT_CONFIG.account_id)
    for transaction in CLIENT_CONFIG.client_api.request(request):
        print(transaction)

def get_transaction_history():
    from oandapyV20.endpoints import transactions
    import pandas as pd
    request = transactions.TransactionList(accountID=CLIENT_CONFIG.account_id,params={'instrument': 'EUR_USD', 'count':10})

    return CLIENT_CONFIG.client_api.request(request)

def calculate_total_unrealised_pnl(positions_dict):
    long_pnl = 0
    short_pnl = 0
    total_pnl = 0

    for position in positions_dict:
        long_unrealized_pnl = float(position['long']['unrealizedPL'])
        short_unrealized_pnl = float(position['short']['unrealizedPL'])

        long_pnl += long_unrealized_pnl
        short_pnl += short_unrealized_pnl
        total_pnl = long_pnl + short_pnl

    return long_pnl, short_pnl, total_pnl

def get_current_balance():
    request = AccountDetails(accountID=CLIENT_CONFIG.account_id)
    response = CLIENT_CONFIG.client_api.request(request)

    if response and 'account' in response:
        account_info = response['account']
        balance = float(account_info['balance'])
        return balance

def get_pending_trades_num():
    request = orders.OrdersPending(accountID=CLIENT_CONFIG.account_id)
    response = CLIENT_CONFIG.client_api.request(request)
    return len(response['orders'])

def place_market_order(instrument, units, take_profit_price, stop_loss_price):
    data = {
        "order": {
            "units": str(units),
            "instrument": instrument,
            "timeInForce": "FOK",
            "type": "MARKET",
            "positionFill": "DEFAULT",
            "takeProfitOnFill": {
                "price": str(float(take_profit_price)),
            },
            "stopLossOnFill": {
                "price": str(float(stop_loss_price)),
            }
        }
    }
    
    try:
        request = orders.OrderCreate(CLIENT_CONFIG.account_id, data=data)
        response = CLIENT_CONFIG.client_api.request(request)
        logger.info("Oanda Orders placed successfully!")
        subject = "Oanda Trades Initiated"
        body = "Oanda Trades Initiated"
        # send_email_notification(subject, body)
    except V20Error as e:
        logger.info("Error placing Oanda orders:")
        logger.info(e)
        subject = "Failed to Take Oanda Trades"
        body = "Failed to Take Oanda Trades"
        # send_email_notification(subject, body)


def close_all_trades(client, account_id):
    # Get a list of all open trades for the account
    trades_request = trades.OpenTrades(accountID=account_id)
    response = client.request(trades_request)

    if len(response['trades']) > 0:
        for trade in response['trades']:
            trade_id = trade['id']
            try:
                # Create a market order to close the trade
                data = {
                    "units": "ALL",
                }
                order_request = trades.TradeClose(accountID=account_id, tradeID=trade_id, data=data)
                response = client.request(order_request)
                logger.info(f"Trade {trade_id} closed successfully.")
            except V20Error as e:
                logger.info(f"Failed to close trade {trade_id}. Error: {e}")
    else:
        logger.info("No open trades to close.")
def fetch_recent_transactions_df(n_rows=100):
    # Set up the client and authentication
    # Create a request to get transactions
    r = transactions.TransactionList(CLIENT_CONFIG.account_id)
    # Fetch the transactions
    try:
        response = CLIENT_CONFIG.client_api.request(r)
    except V20Error as err:
        print("Error encountered: ", err)
        return None
    last_transaction_id = int(response.get('lastTransactionID', 0))
    if last_transaction_id == 0:
        return None
    min_transaction_id = max(0, last_transaction_id - n_rows)
    r = transactions.TransactionsSinceID(CLIENT_CONFIG.account_id, {"id": min_transaction_id})
    response = CLIENT_CONFIG.client_api.request(r)
    transactions_resp:list[dict] = response.get('transactions', [])
    # generate a dataframe
    df = pd.DataFrame(transactions_resp)[['time', 'type', 'reason', 'units', 'price', 'closedTradeID', 'tradeID']]
    # combine the tradeID and closedTradeID
    df['tradeID'] = df['tradeID'].combine_first(df['closedTradeID'])
    # drop the closedTradeID column
    df.drop(columns=['closedTradeID'], inplace=True)
    # convert the time column to datetime
    df['time'] = pd.to_datetime(df['time'])
    # sort the dataframe by most recent time
    df.sort_values(by='time', ascending=False, inplace=True)
    # time should display as "%Y-%m-%d %H:%M:%S"
    df['time'] = df['time'].dt.strftime("%Y-%m-%d %H:%M:%S")
    #df.dropna(inplace=True)
    #print(df.columns.to_list())
    return df
def fetch_trade_markers(last_transaction_id=0, from_date=None, to_date=None):
    # Create a request to get transactions
    params = {}
    if last_transaction_id is not None:
        params["id"] = last_transaction_id
    if from_date is not None:
        params["from"] = from_date
    if to_date is not None:
        params["to"] = to_date
    
    r = transactions.TransactionsSinceID(CLIENT_CONFIG.account_id, params)

    # Fetch the transactions
    try:
        response = CLIENT_CONFIG.client_api.request(r)
    except V20Error as err:
        print("Error encountered: ", err)
        return None
    else:
        transactions_resp:list = response.get('transactions', [])
        #early break
        transactions_resp.reverse()
        markers = []
        current_time = time.time()
        def get_granularity_seconds(granularity):
            _type = granularity[0]
            _unit = int(granularity[1:])
            multiplier = {"S": 1, "M": 60, "H": 3600, "D": 86400}
            return _unit * multiplier[_type]
        threshold_time = current_time - TRADE_CONFIG.lookback_count * get_granularity_seconds(TRADE_CONFIG.granularity)
        transactions_resp_df = pd.DataFrame(transactions_resp)
        del transactions_resp
        transactions_resp_df = transactions_resp_df[transactions_resp_df['type'].isin(['ORDER_FILL', 'MARKET_ORDER']) & (transactions_resp_df['instrument'] == TRADE_CONFIG.instrument)]
        transactions_resp_df['time'] = transactions_resp_df['time'].apply(lambda x: isoparse(x.split(".")[0]+"Z").timestamp())
        transactions_resp_df = transactions_resp_df[transactions_resp_df['time'] > threshold_time]
        transactions_resp_df['units'] = transactions_resp_df['units'].astype(int)
        transactions_resp_df['buyorsell'] = np.where(transactions_resp_df['units'] > 0,
                                                        'buy',
                                                        np.where(transactions_resp_df['units'] < 0, 'sell', None))
        transactions_resp_df['position'] = np.where(transactions_resp_df['buyorsell'] == 'sell', 'aboveBar', 'belowBar')
        transactions_resp_df['color'] = np.where(transactions_resp_df['buyorsell'] == 'sell', 'rgb(244, 63, 94)', 'rgb(16, 185, 129)')
        transactions_resp_df['shape'] = np.where(transactions_resp_df['buyorsell'] == 'sell', 'arrowDown', 'arrowUp')
        transactions_resp_df['text'] = transactions_resp_df['buyorsell'] + " " + transactions_resp_df['units'].abs().astype(str) + " units"
        markers = transactions_resp_df[['time', 'position', 'color', 'shape', 'text']].to_dict(orient='records')
        #print(markers)
        # # convert time to seconds
        # # print strftime
        # # Iterate over transactions and extract buy/sell actions
        # for transaction in transactions_resp:
        #     if transaction['type'] in ('ORDER_FILL', 'MARKET_ORDER') and transaction['instrument'] == TRADE_CONFIG.instrument:  # Check transaction types
        #         _time = transaction['time']
        #         # get rid of milliseconds
        #         _time = _time.split(".")[0] + "Z"
        #         _second_time = isoparse(_time).timestamp()
        #         #print(_time,_second_time ,dt.fromtimestamp(_second_time, tz=timezone.utc).isoformat())
        #         #print(threshold_time,dt.fromtimestamp(threshold_time, tz=timezone.utc).isoformat(), dt.fromtimestamp(current_time, tz=timezone.utc).isoformat())
        #         if _second_time < threshold_time:
        #             continue
        #         _units = int(transaction['units'])
        #         _buyorsell = 'buy' if _units > 0 else 'sell' if _units < 0 else None
        #         _position = 'aboveBar' if _buyorsell == 'sell' else 'belowBar'
        #         _color = "rgb(244, 63, 94)" if _buyorsell == "sell" else "rgb(16, 185, 129)"
        #         _shape = "arrowDown" if _buyorsell == "sell" else "arrowUp"
        #         _text = f"{_buyorsell} {abs(_units)} units"
        #         # Only add markers for buy or sell actions
        #         if _position:
        #             marker = {'time': _second_time, 'position': _position, 'color': _color, 'shape': _shape, 'text': _text}
        #             markers.append(marker)
        # if markers is empty, we need to add a dummy transparent marker to avoid error
        if not markers:
            markers.append({'time': current_time, 'position': 'aboveBar', 'color': 'rgba(0,0,0,0)', 'shape': 'arrowUp', 'text': ''})
        return markers
    
def get_instrument_positions(instrument):
    request = positions.OpenPositions(accountID=CLIENT_CONFIG.account_id)
    response = CLIENT_CONFIG.client_api.request(request).get("positions", [])
    return response[0] if response else {}

if __name__ == "__main__":
    print(get_instrument_positions('EUR_USD'))