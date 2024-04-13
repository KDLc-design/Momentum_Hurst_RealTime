from dash import html, dcc, Output, Input, ctx, State
from dash.dependencies import ClientsideFunction
from datetime import datetime as dt, timezone
from dash.exceptions import PreventUpdate
from services.utils import fetch_data, fetch_trade_markers, fetch_recent_transactions_df, get_pending_trades_num, run_trading_cycle, close_all_trades, get_instrument_positions
from configs.server_conf import logger, app
from configs.oanda_conf import CLIENT_CONFIG, TRADE_CONFIG
from pages.landing_page import landingPage
from pages.dashboard_page import dashboardPage
# from pages.analysis_page import analysisInitialPage, analysisDetailPage
from components.figures import create_line_chart
from data.store import transactions_df, benchmark_returns_list, strategy_returns_list, indicators_lists_dict, list_dequeue_and_append
app.clientside_callback(
    ClientsideFunction(
        namespace="clientside", function_name="transitionToDashboardPage"
    ),
    Output("url", "pathname", allow_duplicate=True),
    [Input("landing-page-explore-now-btn", "n_clicks")],
    prevent_initial_call=True,
)

app.clientside_callback(
    ClientsideFunction(
        namespace="clientside", function_name="transitionToAnalysisPage"
    ),
    Output("url", "pathname", allow_duplicate=True),
    [Input("demo-btn", "n_clicks")],
    prevent_initial_call=True,
)

app.clientside_callback(
    ClientsideFunction(namespace="clientside", function_name="setupCustomScroll"),
    Output(
        "dummy-div-for-analysis-page-scroll-snap", "children"
    ),  # This output can be an invisible dummy div
    Input(
        "analysis-page-scroll-container", "children"
    ),  # Assuming 'your-container-id' identifies the dynamic container
    # prevent_initial_call=True
)


@app.callback(
    Output("landing-page-candlestick-chart", "seriesData"),
    Input("landing-page-candlestick-chart-interval", "n_intervals"),
    prevent_initial_call=True,
)
def update_landing_page_candlestick(
    *args
) -> list[list[dict]]:
    """Update the candlestick chart on the landing page. Either by clicking on the navbar or by the interval dynamic update.

    Args:
        seriesData (list[list[dict]]): series data of tmvlwc.
        nIntervals (int): number of interval.

    Returns:
        list[list[dict]]: updated series data.
    """
    return [fetch_data(TRADE_CONFIG.instrument, TRADE_CONFIG.lookback_count)]
#import time
@app.callback(
    Output("dashboard-page-candlestick-chart", "seriesMarkers"),
    Output("dashboard-page-candlestick-chart", "seriesData"),
    Output("infinite-grid-transactions", "rowData"),
    Output("primary-stats-table-pending-trades","children"),
    Output("returns-comparison-line-fig", "figure"),
    Output("hurst-line-fig", "figure"),
    Output("momentums-line-fig", "figure"),
    Output("rsi-line-fig", "figure"),
    Output("volatility-line-fig", "figure"),
    Input("dashboard-page-candlestick-chart-interval", "n_intervals"),
    prevent_initial_call=True,
)
def update_dashboard_primary_page(*args) -> list[list[dict]]:
    """Update the candlestick chart on the landing page. Either by clicking on the navbar or by the interval dynamic update.

    Args:
        seriesData (list[list[dict]]): series data of tmvlwc.
        nIntervals (int): number of interval.

    Returns:
        list[list[dict]]: updated series data.
    """
    #curr_time  = time.time()
    global transactions_df, indicators_lists_dict, benchmark_returns_list, strategy_returns_list
    transactions_df = fetch_recent_transactions_df()
    pending_trades_num = get_pending_trades_num()
    markers = fetch_trade_markers(last_transaction_id=800)
    # if length does not match, meaning lookback_count changed. initialize fetch.
    is_initial_fetch = False
    if indicators_lists_dict["hurst"] and len(indicators_lists_dict["hurst"]) != TRADE_CONFIG.lookback_count:
        indicators_lists_dict = {
            "hurst": [],
            "short_term_momentum": [],
            "long_term_momentum": [],
            "rsi": [],
            "volatility": [],
        }
        is_initial_fetch = True
    candlestick_data, indicators_lists, bb_data = fetch_data(TRADE_CONFIG.instrument, TRADE_CONFIG.lookback_count, include_indicators=True, is_initial_fetch=is_initial_fetch, include_bollinger_bands=True)
    bb_hband, bb_lband = bb_data
    last_point = candlestick_data[-1]
    # convert to RFC3339
    last_point_time = dt.fromtimestamp(last_point["time"], tz=timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f000Z')
    list_dequeue_and_append(benchmark_returns_list, TRADE_CONFIG.lookback_count, {"time": last_point_time, "value": float(last_point["close"])})
    list_dequeue_and_append(strategy_returns_list, TRADE_CONFIG.lookback_count, {"time": last_point_time, "value": float(CLIENT_CONFIG.current_balance / CLIENT_CONFIG.initial_balance)})
    if is_initial_fetch:
        for _i, key in enumerate(indicators_lists_dict):
            indicators_lists_dict[key] = indicators_lists[_i]
    else:
        for _i, key in enumerate(indicators_lists_dict):
            list_dequeue_and_append(indicators_lists_dict[key], TRADE_CONFIG.lookback_count, indicators_lists[_i][0])
    returns_comparison_line_fig = create_line_chart(
        [benchmark_returns_list, strategy_returns_list],
        "Returns",
        ["rgb(16, 185, 129)", "rgb(244, 63, 94)"],
        ["Benchmark", "Strategy"],
    )
    # hurst figure
    hurst_fig = create_line_chart(
        [indicators_lists_dict["hurst"]],
        "Hurst Exponent",
        ["rgb(16, 185, 129)"],
        ["Hurst Exponent"],
    )
    # momentums figure
    momentums_fig = create_line_chart(
        [indicators_lists_dict["short_term_momentum"], indicators_lists_dict["long_term_momentum"]],
        "Momentum",
        ["rgb(16, 185, 129)", "rgb(244, 63, 94)"],
        ["Short-term Momentum", "Long-term Momentum"],
    )
    rsi_fig = create_line_chart(
        [indicators_lists_dict["rsi"]],
        "RSI",
        ["rgb(16, 185, 129)"],
        ["RSI"],
    )
    volatility_fig = create_line_chart(
        [indicators_lists_dict["volatility"]],
        "Volatility",
        ["rgb(16, 185, 129)"],
        ["Volatility"],
    )
    #print("Time taken: ", time.time() - curr_time)
    return [markers], [candlestick_data, bb_hband, bb_lband], transactions_df.to_dict("records"), str(pending_trades_num), returns_comparison_line_fig, hurst_fig, momentums_fig, rsi_fig, volatility_fig

@app.callback(
    Output("landing-page-container", "className"),
    Input("landing-page-explore-now-btn", "n_clicks"),
    State("url", "pathname"),
    State("landing-page-container", "className"),
    prevent_initial_call=True,
)
def trigger_landingPage_transition(n_clicks: int, pathname: str, classname: str):
    if n_clicks and pathname == "/":
        # Add transition animation
        classname += (
            " transition duration-[600ms] ease-in-out -translate-x-full opacity-0"
        )
        return classname
    raise PreventUpdate


@app.callback(
    Output("dashboard-page-container", "className"),
    Input("demo-btn", "n_clicks"),
    State("url", "pathname"),
    State("dashboard-page-container", "className"),
    prevent_initial_call=True,
)
def trigger_dashboardPage_transition(n_clicks: int, pathname: str, classname: str):
    if n_clicks and pathname == "/dashboard":
        # remove 'animate-slide-in-y animate-delay-700' from the classname
        classname = classname.replace("animate-slide-in-x animate-delay-700", "")
        # Add transition animation
        classname += " transition duration-[300ms] ease-in-out animate-slide-out-x animate-500 opacity-0"
        return classname
    raise PreventUpdate


@app.callback(
    Output("content-container", "children"),
    Input("url", "pathname"),
)
def display_page(pathname: str):
    return dashboardPage() if pathname == "/dashboard" else landingPage()

@app.callback(
    Output("dashboard-page-top-drawer", "opened"),
    Input("dashboard-page-top-drawer-btn", "n_clicks"),
    prevent_initial_call=True,
)
def top_drawer_open(n_clicks):
    return True
@app.callback(
    Output("dashboard-page-bottom-drawer", "opened"),
    Input("dashboard-page-bottom-drawer-btn", "n_clicks"),
    prevent_initial_call=True,
)
def bottom_drawer_open(n_clicks):
    return True
def update_log():
    with open("app.log", "r") as f:
        lines = f.readlines()[-100:]
        lines.reverse()
    return html.Div([html.P(line) for line in lines], className="w-full h-full scrollableY")

@app.callback(
    Output("dashboard-page-trade-title", "children"),
    Input("dashboard-page-start-trade-btn", "n_clicks"),
    Input("dashboard-page-pause-trade-btn", "n_clicks"),
    Input("dashboard-page-kill-trade-btn", "n_clicks"),
    prevent_initial_call=True,
)
def update_trade_title(*args):
    clicked_btn = ctx.triggered[0]["prop_id"].split(".")[0]
    if clicked_btn == "dashboard-page-start-trade-btn":
        return  html.P(
                    [
                        "Trading ",
                        html.Span(
                            TRADE_CONFIG.instrument,
                            className="text-slate-400 underline font-semibold hover:text-slate-200 cursor-pointer transition duration-200 ease-in-out",
                        ),
                        " with ",
                        html.Span(
                            "Oanda API",
                            className="text-slate-400 underline font-semibold hover:text-slate-200 cursor-pointer transition duration-200 ease-in-out",
                        ),
                        "...",
                    ],
                    className="animate-pulse text-slate-400 text-lg select-none",
                )
    else:
        return html.P(
            [
                "Ready to trade...",
            ],
            className="text-slate-400 text-lg select-none",
        )

is_trading_flag = False

@app.callback(
    Output("dashboard-page-log", "children"),
    Output("primary-stats-table-current-balance", "children"),
    Output("primary-stats-table-current-pnl", "children"),
    Input("dashboard-page-start-trade-btn", "n_clicks"),
    Input("dashboard-page-pause-trade-btn", "n_clicks"),
    Input("dashboard-page-kill-trade-btn", "n_clicks"),
    Input("dashboard-page-trade-interval", "n_intervals"),
    prevent_initial_call=True,
)
def real_time_trade(*args):
    global is_trading_flag
    if not args:
        raise PreventUpdate
    clicked_btn = ctx.triggered[0]["prop_id"].split(".")[0]
    if is_trading_flag and clicked_btn == "dashboard-page-start-trade-btn":
        return update_log(), CLIENT_CONFIG.current_balance, CLIENT_CONFIG.current_balance - CLIENT_CONFIG.initial_balance
    # if (clicked start button and not trading) or already trading
    if clicked_btn == "dashboard-page-start-trade-btn":
        logger.info("Starting trading...")
        ret_dict = run_trading_cycle()
        is_trading_flag = True
        return update_log(), CLIENT_CONFIG.current_balance, CLIENT_CONFIG.current_balance - CLIENT_CONFIG.initial_balance
    elif clicked_btn == "dashboard-page-pause-trade-btn" and is_trading_flag:
        logger.info("Pausing trading...")
        is_trading_flag = False
        return update_log(), CLIENT_CONFIG.current_balance, CLIENT_CONFIG.current_balance - CLIENT_CONFIG.initial_balance
    elif clicked_btn == "dashboard-page-kill-trade-btn":
        logger.info("Closing all trades...")
        # close all trades and stop trading
        close_all_trades(CLIENT_CONFIG.client_api, CLIENT_CONFIG.account_id)
        is_trading_flag = False
        return update_log(), CLIENT_CONFIG.current_balance, CLIENT_CONFIG.current_balance - CLIENT_CONFIG.initial_balance
    elif is_trading_flag:
        run_trading_cycle()
        return update_log(), CLIENT_CONFIG.current_balance, CLIENT_CONFIG.current_balance - CLIENT_CONFIG.initial_balance
    else:
        raise PreventUpdate
@app.callback(
    Output('oanda-access-token-input', 'value'),
    Input('oanda-access-token-input', 'value')
)
def update_access_token(value):
    CLIENT_CONFIG.access_token = value
    return value

# Callback for updating account ID
@app.callback(
    Output('oanda-account-id-input', 'value'),
    Input('oanda-account-id-input', 'value')
)
def update_account_id(value):
    CLIENT_CONFIG.account_id = value
    return value

# Callback for updating environment
@app.callback(
    Output('oanda-account-environment-input', 'value'),
    Input('oanda-account-environment-input', 'value')
)
def update_environment(value):
    CLIENT_CONFIG.environment = value
    return value
@app.callback(
    Output('trade-instrument-input', 'value'),
    Input('trade-instrument-input', 'value')
)
def update_instrument(value):
    TRADE_CONFIG.instrument = value
    logger.info(f"Updated instrument to {value}")
    return value

# Callback for updating lookback count
@app.callback(
    Output('trade-lookback-count-input', 'value'),
    Input('trade-lookback-count-input', 'value')
)
def update_lookback_count(value):
    TRADE_CONFIG.lookback_count = value
    return value

# Callback for updating short window
@app.callback(
    Output('trade-short-window-input', 'value'),
    Input('trade-short-window-input', 'value')
)
def update_short_window(value):
    TRADE_CONFIG.st_period = value
    return value

# Callback for updating long window
@app.callback(
    Output('trade-long-window-input', 'value'),
    Input('trade-long-window-input', 'value')
)
def update_long_window(value):
    TRADE_CONFIG.lt_period = value
    return value

# Callback for updating hurst window
@app.callback(
    Output('trade-hurst-window-input', 'value'),
    Input('trade-hurst-window-input', 'value')
)
def update_hurst_window(value):
    TRADE_CONFIG.hurst_period = value
    return value



# Callback for updating risk factor
@app.callback(
    Output('trade-risk-factor-input', 'value'),
    Input('trade-risk-factor-input', 'value')
)
def update_risk_factor(value):
    try:
        risk_factor = float(value)
        TRADE_CONFIG.risk_factor = risk_factor
        return risk_factor
    except ValueError:
        raise PreventUpdate

# Callback for updating risk reward
@app.callback(
    Output('trade-risk-reward-input', 'value'),
    Input('trade-risk-reward-input', 'value')
)
def update_risk_reward(value):
    try:
        risk_reward = float(value)
        TRADE_CONFIG.risk_reward = risk_reward
        return risk_reward
    except ValueError:
        raise PreventUpdate

# Callback for updating time interval
@app.callback(
    Output('trade-granularity-input', 'value'),
    Input('trade-granularity-input', 'value')
)
def update_granularity(value):
    try:
        granularity = str(value)
        TRADE_CONFIG.granularity = granularity
        return granularity
    except ValueError:
        raise PreventUpdate

# Callback for updating stoploss PnL
@app.callback(
    Output('trade-stoploss-pnl-input', 'value'),
    [Input('trade-risk-factor-input', 'value'),
     State('trade-stoploss-pnl-input', 'value')]
)
def update_stoploss_pnl(risk_factor_value, stoploss_pnl_value):
    try:
        risk_factor = float(risk_factor_value)
        stoploss_pnl = CLIENT_CONFIG.initial_balance * risk_factor
        return stoploss_pnl
    except ValueError:
        raise PreventUpdate

# Callback for updating target PnL
@app.callback(
    Output('trade-target-pnl-input', 'value'),
    [Input('trade-risk-factor-input', 'value'),
     Input('trade-risk-reward-input', 'value'),
     State('trade-target-pnl-input', 'value')]
)
def update_target_pnl(risk_factor_value, risk_reward_value, target_pnl_value):
    try:
        risk_factor = float(risk_factor_value)
        risk_reward = float(risk_reward_value)
        target_pnl = CLIENT_CONFIG.initial_balance * risk_factor * risk_reward
        return target_pnl
    except ValueError:
        raise PreventUpdate
app.layout = html.Div(
    [
        # comment this when using testPage
        dcc.Location(
            id="url",
            refresh=False,
            pathname="/",
        ),
        html.Div(
            [landingPage()],
            id="content-container",
            className="w-dvw h-dvh overflow-hidden",
        ),
    ],
    id="main-layout",
    className="w-dvw h-dvh overflow-hidden bg-slate-900 min-h-[400px]",
)

@app.callback(
    Output("open-position-stats-table-long-units", "children"),
    Output("open-position-stats-table-short-units", "children"),
    Output("open-position-stats-table-long-avg-price", "children"),
    Output("open-position-stats-table-short-avg-price", "children"),
    Output("open-position-stats-table-long-unrealized-pnl", "children"),
    Output("open-position-stats-table-short-unrealized-pnl", "children"),
    Output("open-position-stats-table-long-margin-used", "children"),
    Output("open-position-stats-table-short-margin-used", "children"),
    Input("dashboard-page-trade-interval", "n_intervals"),
)
def update_open_position_stats(n_intervals):
    resp_dict:dict = get_instrument_positions(TRADE_CONFIG.instrument)
    # when no positions open
    if not resp_dict:
        return 0, 0, 0, 0, 0, 0, 0, 0
    long_units = resp_dict["long"].get("units", 0)
    short_units = abs(int(resp_dict["short"].get("units", 0)))
    long_avg_price = resp_dict["long"].get("averagePrice", 0)
    short_avg_price = resp_dict["short"].get("averagePrice", 0)
    long_unrealized_pnl = resp_dict["long"].get("unrealizedPL", 0)
    short_unrealized_pnl = resp_dict["short"].get("unrealizedPL", 0)
    long_margin_used = resp_dict["long"].get("marginUsed", 0)
    short_margin_used = resp_dict["short"].get("marginUsed", 0)
    return long_units, short_units, long_avg_price, short_avg_price, long_unrealized_pnl, short_unrealized_pnl, long_margin_used, short_margin_used
if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0")