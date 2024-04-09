import oandapyV20.endpoints.positions as positions
import oandapyV20.endpoints.orders as orders
import oandapyV20.endpoints.trades as trades
import oandapyV20.endpoints.pricing as pricing
from oandapyV20.endpoints.accounts import AccountDetails
from oandapyV20.exceptions import V20Error
# from notification import send_email_notification

from configs.oanda_conf import CLIENT_CONFIG
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
