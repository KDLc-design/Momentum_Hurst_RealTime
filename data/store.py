from services.strategy_utils import run_strategy
from services.risk_manager import fetch_recent_transactions_df
from configs.oanda_conf import TRADE_CONFIG
results_df, metrics_df, trades_df, full_trade_df = run_strategy()
transactions_df = fetch_recent_transactions_df()
strategy_returns = []
benchmark_returns = []