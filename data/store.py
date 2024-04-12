from services.risk_manager import fetch_recent_transactions_df

transactions_df = fetch_recent_transactions_df()
strategy_returns_list = []
benchmark_returns_list = []
indicators_lists_dict = {
    "hurst": [],
    "short_term_momentum": [],
    "long_term_momentum": [],
    "rsi": [],
}
def list_dequeue_and_append(_list:list, _max_len:int, _new_item):
    if len(_list) > _max_len:
        _list.pop(0)
    _list.append(_new_item)
    return _list