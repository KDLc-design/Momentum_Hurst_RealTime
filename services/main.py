from services.signal_generator import generate_signal
from services.risk_manager import get_quantity, place_market_order, get_open_positions, get_current_balance, \
    calculate_total_unrealised_pnl, close_all_trades
from notification import send_email_notification
import time
from configs.oanda_conf import OANDA_ACCESS_TOKEN, OANDA_ACCOUNT_ID, OANDA_CLIENT_API

# helper variables
instrument = 'EUR_USD'
lookback_count = 200
# Changed parameters
st_period = 5
lt_period = 21
hurst_period = 200

inposition = False

opening_balance = get_current_balance()
risk_factor = 0.016 / 100
stoploss_pnl = opening_balance * risk_factor
risk_reward = 0.75  # 3/4
target_pnl = stoploss_pnl * risk_reward

last_print_time = time.time()
time_interval = 1 * 60

print("==" * 25)
print("")
print("==" * 25)
print("Starting balance : {:.2f}".format(opening_balance))
print("Take Profit initial : {:.2f}".format(target_pnl))
print("Stop loss initial : {:.2f}".format(stoploss_pnl))
print("==" * 25)


def find_quantities_and_trade(instrument, trade_direction):
    global takeprofit
    global stoploss
    global inposition

    stoploss, takeprofit, quantity = get_quantity(instrument, trade_direction)

    print("==" * 25)
    print("Oanda quantities")
    print("Instrument:", instrument, " | Vol :", quantity, " | StopLoss :", stoploss, " | Takeprofit :", takeprofit)
    # Place orders
    place_market_order(instrument, quantity, takeprofit, stoploss)

    inposition = True
    time.sleep(3)


def update_trade_status():
    global inposition
    global opening_balance
    global stoploss_pnl
    global target_pnl
    global risk_factor
    global risk_reward

    inposition = False
    opening_balance = get_current_balance()
    risk_factor = 0.016 / 100
    stoploss_pnl = opening_balance * risk_factor
    risk_reward = 0.75
    target_pnl = stoploss_pnl * risk_reward


while True:
    try:
        # we will trade only if NOT in position
        if not inposition:
            trade_direction = generate_signal(instrument, lookback_count, st_period, lt_period, hurst_period)
            print("Trade Direction: ", trade_direction)
            if trade_direction is None or trade_direction == "HOLD":
                pass
            else:
                print("Found opportunity in {}".format(instrument))
                find_quantities_and_trade(instrument, trade_direction)
                # send_email_notification()

        if inposition:
            positions_dict = get_open_positions()
            long_pnl, short_pnl, total_pnl = calculate_total_unrealised_pnl(positions_dict)

            current_time = time.time()
            # check pnl
            if current_time - last_print_time >= time_interval:
                print(f" Target:  {target_pnl:.2f} | StopLoss: {stoploss_pnl :.2f} | PNL:  {total_pnl:.2f} ")
                last_print_time = current_time
            # exit check
            if (total_pnl > target_pnl) or (total_pnl < -stoploss_pnl):
                if total_pnl > target_pnl:
                    msg = f"Profit Trade, Target : {target_pnl:.2f} | Actual: {total_pnl:.2f}"
                elif total_pnl < -stoploss_pnl:
                    msg = f"Loss Trade, Target:  {target_pnl:.2f} | Actual: {total_pnl:.2f} "
                print(msg)
                close_all_trades(OANDA_CLIENT_API, OANDA_ACCOUNT_ID)
                print("Closing all Trades")
                print("Current balance: {:.2f}".format(get_current_balance()))

                update_trade_status()

                subject = "Closing Trades"
                body = msg
                # send_email_notification(subject, body)

            else:
                pass
    except Exception as e:
        print(f"An error occurred: {e}")
        pass

    time.sleep(5)
