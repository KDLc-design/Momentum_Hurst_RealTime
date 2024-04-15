import os
import sys
#setting the path to the root directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from services.signal_generator import generate_signal, calculate_all_indicators
from services.risk_manager import get_quantity, place_market_order, get_open_positions, get_current_balance, \
    calculate_total_unrealised_pnl, close_all_trades
from services.notification import send_email_notification
import time
from configs.oanda_conf import CLIENT_CONFIG, TRADE_CONFIG
from configs.server_conf import logger
# # helper variables
# instrument = 'EUR_USD'
# lookback_count = 200
# # Changed parameters
# st_period = 5
# lt_period = 21
# hurst_period = 200

# inposition = False

# risk_factor = 0.016 / 100
# risk_reward = 0.75  # 3/4
# time_interval = 1 * 60

opening_balance = CLIENT_CONFIG.initial_balance
stoploss_pnl = opening_balance * TRADE_CONFIG.risk_factor
target_pnl = stoploss_pnl * TRADE_CONFIG.risk_reward
last_print_time = time.time()

logger.info("Starting balance : {:.2f}".format(opening_balance))
logger.info("Take Profit initial : {:.2f}".format(target_pnl))
logger.info("Stop loss initial : {:.2f}".format(stoploss_pnl))


def find_quantities_and_trade(instrument, trade_direction):

    stoploss, takeprofit, quantity = get_quantity(instrument, trade_direction)

    logger.info("--" * 5)
    logger.info("Oanda quantities")
    logger.info(f"Instrument: {instrument} | Vol : {quantity} | StopLoss : {stoploss} | Takeprofit : {takeprofit}")
    # Place orders
    place_market_order(instrument, quantity, takeprofit, stoploss)

    TRADE_CONFIG.inposition = True
    time.sleep(3)


def update_trade_status():
    global stoploss_pnl, target_pnl, opening_balance
    TRADE_CONFIG.inposition = False
    opening_balance = CLIENT_CONFIG.current_balance
    risk_factor = 0.016 / 100
    stoploss_pnl = opening_balance * risk_factor
    risk_reward = 0.75
    target_pnl = stoploss_pnl * risk_reward

# Assume all imports and initializations are done above this point

def run_trading_cycle():
    global opening_balance, stoploss_pnl, target_pnl, last_print_time
    
    # try:
    if not TRADE_CONFIG.inposition:
        trade_direction = generate_signal(TRADE_CONFIG.instrument, TRADE_CONFIG.lookback_count, TRADE_CONFIG.st_period,TRADE_CONFIG.lt_period, TRADE_CONFIG.hurst_period)
        logger.info(f"----------")
        logger.info(f"Trade Direction: {trade_direction}")
        if trade_direction not in [None, "HOLD"]:
            logger.info(f"Found opportunity in {TRADE_CONFIG.instrument}")
            find_quantities_and_trade(TRADE_CONFIG.instrument, trade_direction)
            # send_email_notification()

    else:
        positions_dict = get_open_positions()
        long_pnl, short_pnl, total_pnl = calculate_total_unrealised_pnl(positions_dict)
        current_time = time.time()

        if current_time - last_print_time >= TRADE_CONFIG.time_interval:
            logger.info(f" Target:  {target_pnl:.2f} | StopLoss: {stoploss_pnl:.2f} | PNL:  {total_pnl:.2f} ")
            last_print_time = current_time

        if (total_pnl > target_pnl) or (total_pnl < -stoploss_pnl):
            msg = ""
            if total_pnl > target_pnl:
                msg = f"Profit Trade, Target : {target_pnl:.2f} | Actual: {total_pnl:.2f}"
            elif total_pnl < -stoploss_pnl:
                msg = f"Loss Trade, Target:  {target_pnl:.2f} | Actual: {total_pnl:.2f} "
            logger.info(msg)
            close_all_trades(CLIENT_CONFIG.client_api, CLIENT_CONFIG.account_id)
            logger.info("Closing all Trades")
            logger.info("Current balance: {:.2f}".format(get_current_balance()))

            update_trade_status()
            
            subject = "Closing Trades"
            body = msg
            # send_email_notification(subject, body)

    # except Exception as e:
    #     logger.info(f"An error occurred: {e}")
    
    return {
        'inposition': TRADE_CONFIG.inposition,
        'opening_balance': opening_balance,
        'stoploss_pnl': stoploss_pnl,
        'target_pnl': target_pnl
    }
if __name__ == "__main__":
    from oandapyV20.endpoints import transactions
    request = transactions.TransactionsSinceID(CLIENT_CONFIG.account_id, params={"id": 1})
    print(CLIENT_CONFIG.client_api.request(request))
# while True:
#     try:
#         # we will trade only if NOT in position
#         if not inposition:
#             trade_direction = generate_signal(instrument, lookback_count, st_period, lt_period, hurst_period)
#             logger.info("Trade Direction: ", trade_direction)
#             if trade_direction is None or trade_direction == "HOLD":
#                 pass
#             else:
#                 logger.info("Found opportunity in {}".format(instrument))
#                 find_quantities_and_trade(instrument, trade_direction)
#                 # send_email_notification()

#         if inposition:
#             positions_dict = get_open_positions()
#             long_pnl, short_pnl, total_pnl = calculate_total_unrealised_pnl(positions_dict)

#             current_time = time.time()
#             # check pnl
#             if current_time - last_print_time >= time_interval:
#                 logger.info(f" Target:  {target_pnl:.2f} | StopLoss: {stoploss_pnl :.2f} | PNL:  {total_pnl:.2f} ")
#                 last_print_time = current_time
#             # exit check
#             if (total_pnl > target_pnl) or (total_pnl < -stoploss_pnl):
#                 if total_pnl > target_pnl:
#                     msg = f"Profit Trade, Target : {target_pnl:.2f} | Actual: {total_pnl:.2f}"
#                 elif total_pnl < -stoploss_pnl:
#                     msg = f"Loss Trade, Target:  {target_pnl:.2f} | Actual: {total_pnl:.2f} "
#                 logger.info(msg)
#                 close_all_trades(CLIENT_CONFIG.client_api, CLIENT_CONFIG.account_id)
#                 logger.info("Closing all Trades")
#                 logger.info("Current balance: {:.2f}".format(get_current_balance()))

#                 update_trade_status()

#                 subject = "Closing Trades"
#                 body = msg
#                 # send_email_notification(subject, body)

#             else:
#                 pass
#     except Exception as e:
#         logger.info(f"An error occurred: {e}")
#         pass

#     time.sleep(5)
