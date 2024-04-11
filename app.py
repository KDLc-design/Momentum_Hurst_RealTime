from dash import Dash, html, dcc, Output, Input, ctx, State
from dash.dependencies import ClientsideFunction
from dash.exceptions import PreventUpdate
import dash_ag_grid as dag
import plotly.express as px
import numpy as np
import pandas as pd
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import dash_tvlwc
import yfinance as yf
import random
import logging
import dash_echarts as dec
from services.strategy_utils import run_strategy, fetch_data
from services.signal_generator import fetch_candlestick_data
from components.common.wrappers import paperWrapperComponent
from datetime import datetime as dt
import plotly.graph_objs as go
from textwrap import dedent
from configs.server_conf import logger, app
from configs.oanda_conf import CLIENT_CONFIG, TRADE_CONFIG
from pages.landing_page import landingPage
from pages.dashboard_page import dashboardPage
from pages.analysis_page import analysisInitialPage, analysisDetailPage
from components.tables import dmcTableComponent
from components.figures import visualisationFiguresGrid
from data.store import trades_df, full_trade_df, transactions_df
from services.main import run_trading_cycle, close_all_trades
from services.risk_manager import fetch_trade_markers, fetch_recent_transactions_df, get_pending_trades_num

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
    # Output("landing-page-candlestick-chart-store", "data"),
    # Input("landing-page-candlestick-chart", "seriesData"),
    Input("landing-page-candlestick-chart-interval", "n_intervals"),
    # State("landing-page-candlestick-chart-store", "data"),
    # Input("navbar-meta", "n_clicks"),
    # Input("navbar-aapl", "n_clicks"),
    # Input("navbar-amzn", "n_clicks"),
    # Input("navbar-nflx", "n_clicks"),
    # Input("navbar-goog", "n_clicks"),
    prevent_initial_call=True,
)
def update_landing_page_candlestick(
    *args#seriesData: list[list[dict]], nIntervals: int, data: dict[list], *args
) -> list[list[dict]]:
    """Update the candlestick chart on the landing page. Either by clicking on the navbar or by the interval dynamic update.

    Args:
        seriesData (list[list[dict]]): series data of tmvlwc.
        nIntervals (int): number of interval.

    Returns:
        list[list[dict]]: updated series data.
    """
    return [fetch_data(TRADE_CONFIG.instrument, TRADE_CONFIG.lookback_count)[0]]

@app.callback(
    Output("dashboard-page-candlestick-chart", "seriesMarkers"),
    Output("dashboard-page-candlestick-chart", "seriesData"),
    Output("infinite-grid-transactions", "rowData"),
    Output("primary-stats-table-pending-trades","children"),
    Output("returns-comparison-line-fig", "figure"),
    # Output("landing-page-candlestick-chart-store", "data"),
    # Input("landing-page-candlestick-chart", "seriesData"),
    Input("dashboard-page-candlestick-chart-interval", "n_intervals"),
    # State("landing-page-candlestick-chart-store", "data"),
    # Input("navbar-meta", "n_clicks"),
    # Input("navbar-aapl", "n_clicks"),
    # Input("navbar-amzn", "n_clicks"),
    # Input("navbar-nflx", "n_clicks"),
    # Input("navbar-goog", "n_clicks"),
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
    # data = fetch_data(TRADE_CONFIG.instrument, TRADE_CONFIG.lookback_count)
    # logger.info(f"Fetching {TRADE_CONFIG.lookback_count} data for {TRADE_CONFIG.instrument}, data size {len(data)}")
    # markers = fetch_trade_markers()
    # logger.info(markers)
    global transactions_df
    transactions_df = fetch_recent_transactions_df()
    pending_trades_num = get_pending_trades_num()
    markers =[ fetch_trade_markers(last_transaction_id=800)]
    candlestick_data, benchmark_data, strategy_returns_data = fetch_data(TRADE_CONFIG.instrument, TRADE_CONFIG.lookback_count)
    benchmark_data = pd.DataFrame(benchmark_data)
    strategy_returns_data = pd.DataFrame(strategy_returns_data)
    # benchmark_data.reset_index(inplace=True)
    # strategy_returns_data.reset_index(inplace=True)
    # ensure float values
    benchmark_data["value"] = benchmark_data["value"].astype(float)
    strategy_returns_data["value"] = strategy_returns_data["value"].astype(float)
    returns_comparison_line_fig = go.Figure()
    returns_comparison_line_fig.add_trace(
        go.Scatter(
            x=benchmark_data['time'],
            y=benchmark_data['value'],
            mode="lines",
            name="Benchmark",
            line=dict(color="rgb(16, 185, 129)"),
        )
    )
    returns_comparison_line_fig.add_trace(
        go.Scatter(
            x=strategy_returns_data['time'],
            y=strategy_returns_data['value'],
            mode="lines",
            name="Strategy",
            line=dict(color="rgb(244, 63, 94)"),
        )
    )
    returns_comparison_line_fig.update_layout(
        autosize=True,
        margin=dict(l=0, r=20, t=10, b=0),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="rgb(100,116,139)"),
        xaxis={"showticklabels": False, "title": "Date", "showgrid": False},
        yaxis={
            "title": "Returns",
            "showgrid": False,
            "zerolinecolor": "rgb(148, 163, 184)",
        },
        showlegend=False,
    )
    
    # print(candlestick_data)
    # print(benchmark_data)
    # print(strategy_returns_data)
    seriesData = [candlestick_data]
    return markers, seriesData, transactions_df.to_dict("records"), str(pending_trades_num), returns_comparison_line_fig

@app.callback(
    Output("analysis-page-inner-container", "children"),
    Input("analysis-page-title-interval", "n_intervals"),
)
def erase_title_dom_and_replace(
    nIntervals: int,
) -> html.Div:
    """Erase the title and replace with the analysis page layout.

    Args:
        nIntervals (int): number of intervals.

    Returns:
        html.Div: analysis page layout.
    """
    if nIntervals == 0 or nIntervals is None:
        raise PreventUpdate
    #logger.info("Erase title and replace with analysis page layout.")
    return analysisDetailPage()


@app.callback(
    Output("analysis-page-infinite-grid-full-trades-container", "children"),
    Input("analysis-page-infinite-grid-full-trades-btn", "n_clicks"),
    prevent_initial_call=True,
)
def show_result_full_trades(nClicks: int) -> dash_tvlwc.Tvlwc:
    if nClicks is None:
        raise PreventUpdate
    return dmcTableComponent(
        "analysis-page-infinite-grid-full-trades"
    )  # tvwlcComponent()


@app.callback(
    Output("analysis-page-infinite-grid-metrics-container", "children"),
    Input("analysis-page-infinite-grid-metrics-btn", "n_clicks"),
    prevent_initial_call=True,
)
def show_result_metrics(nClicks: int) -> dash_tvlwc.Tvlwc:
    if nClicks is None:
        raise PreventUpdate
    return dmcTableComponent("analysis-page-infinite-grid-metrics")  # tvwlcComponent()


@app.callback(
    Output("analysis-page-infinite-grid-full-trades-infinite-output", "children"),
    Input("analysis-page-infinite-grid-full-trades", "selectedRows"),
)
def display_selected_full_trades(selectedRows):
    if selectedRows:
        return [f"You selected id {s['id']} and name {s['name']}" for s in selectedRows]
    raise PreventUpdate


@app.callback(
    Output("analysis-page-infinite-grid-full-trades", "getRowsResponse"),
    Input("analysis-page-infinite-grid-full-trades", "getRowsRequest"),
)
def infinite_scroll_full_trades(request):
    if request is None:
        raise PreventUpdate
    # instead of original ascending order, we use descending order
    total_rows = full_trade_df.shape[0]
    partial = full_trade_df.iloc[
        total_rows - request["endRow"] : total_rows - request["startRow"]
    ][::-1]
    return {"rowData": partial.to_dict("records"), "rowCount": len(full_trade_df.index)}


@app.callback(
    Output("infinite-output-trade", "children"),
    Input("infinite-grid-trade", "selectedRows"),
)
def display_selected_trade(selectedRows):
    if selectedRows:
        return [f"You selected id {s['id']} and name {s['name']}" for s in selectedRows]
    raise PreventUpdate


@app.callback(
    Output("infinite-grid-trade", "getRowsResponse"),
    Input("infinite-grid-trade", "getRowsRequest"),
)
def infinite_scroll_trade(request):
    if request is None:
        raise PreventUpdate
    partial = trades_df.iloc[request["startRow"] : request["endRow"]]
    return {"rowData": partial.to_dict("records"), "rowCount": len(trades_df.index)}







@app.callback(
    Output("analysis-page-visualisation-container", "children"),
    Input("analysis-page-visualisation-btn", "n_clicks"),
)
def show_visualisation_grid(nClicks: int) -> list[html.Div]:
    if nClicks is None:
        raise PreventUpdate
    return visualisationFiguresGrid()



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
    if pathname == "/dashboard":
        #logger.info("Switch to dashboard page.")
        return dashboardPage()
    if pathname == "/analysis":
        # deal with delay by client side js
        # ////time.sleep(0.2)  #! hack way to wait for the transition to finish
        #logger.info("Switch to analysis page.")
        return analysisInitialPage()
    #logger.info(f"Switch to landing page for {pathname}.")
    return landingPage()

# Define the callback to handle form submission
"""@app.callback(
    Output("output-container", "children"),
    [Input("submit-button", "n_clicks")],
    [
        State("stocks-input", "value"),
        State("start-date-picker", "value"),
        State("end-date-picker", "value"),
        State("short-window-input", "value"),
        State("long-window-input", "value"),
        State("hurst-window-input", "value"),
    ],
)
def update_output(
    n_clicks, stocks, start_date, end_date, short_window, long_window, hurst_window
):
    global results_df, metrics_df
    if n_clicks > 0:
        # Process the stocks input into a list
        stocks_list = stocks.split(",")
        # Convert the date strings to actual dates (if necessary)
        start_date_obj = dt.strptime(start_date, "%Y-%m-%d")
        end_date_obj = dt.strptime(end_date, "%Y-%m-%d")
        # Run the strategy function
        results_df, metrics_df = run_strategy(
            stocks_list,
            start_date_obj,
            end_date_obj,
            short_window,
            long_window,
            hurst_window,
        )
        raise PreventUpdate
    raise PreventUpdate"""



@app.callback(
    Output("dashboard-page-drawer", "opened"),
    Input("dashboard-page-drawer-btn", "n_clicks"),
    prevent_initial_call=True,
)
def drawer_demo(n_clicks):
    return True

def update_log():
    with open("app.log", "r") as f:
        lines = f.readlines()[-100:]
        lines.reverse()
    return html.Div([html.P(line) for line in lines], className="w-full h-full scrollableY")
is_trading_flag = False
@app.callback(
    Output("dashboard-page-log", "children"),
    Output("primary-stats-table-current-balance", "children"),
    Output("primary-stats-table-current-pnl", "children"),
    Output("dashboard-page-trade-title", "children"),
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
        return update_log(), CLIENT_CONFIG.current_balance, CLIENT_CONFIG.current_balance - CLIENT_CONFIG.initial_balance, html.P(
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
    # if (clicked start button and not trading) or already trading
    if clicked_btn == "dashboard-page-start-trade-btn":
        logger.info("Starting trading...")
        ret_dict = run_trading_cycle()
        is_trading_flag = True
        return update_log(), CLIENT_CONFIG.current_balance, CLIENT_CONFIG.current_balance - CLIENT_CONFIG.initial_balance, html.P(
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
    elif clicked_btn == "dashboard-page-pause-trade-btn" and is_trading_flag:
        logger.info("Pausing trading...")
        is_trading_flag = False
        return update_log(), CLIENT_CONFIG.current_balance, CLIENT_CONFIG.current_balance - CLIENT_CONFIG.initial_balance, html.P(
            [
                "Ready to trade ",
                html.Span(
                    TRADE_CONFIG.instrument,
                    className="text-slate-400 underline font-semibold hover:text-slate-200 cursor-pointer transition duration-200 ease-in-out",
                ),
                " with ",
                html.Span(
                    "Oanda API",
                    className="text-slate-400 underline font-semibold hover:text-slate-200 cursor-pointer transition duration-200 ease-in-out",
                )
            ],
            className="text-slate-400 text-lg select-none",
        )
    elif clicked_btn == "dashboard-page-kill-trade-btn":
        logger.info("Closing all trades...")
        # close all trades and stop trading
        close_all_trades(CLIENT_CONFIG.client_api, CLIENT_CONFIG.account_id)
        is_trading_flag = False
        return update_log(), CLIENT_CONFIG.current_balance, CLIENT_CONFIG.current_balance - CLIENT_CONFIG.initial_balance, html.P(
                    [
                        "Ready to trade ",
                        html.Span(
                            TRADE_CONFIG.instrument,
                            className="text-slate-400 underline font-semibold hover:text-slate-200 cursor-pointer transition duration-200 ease-in-out",
                        ),
                        " with ",
                        html.Span(
                            "Oanda API",
                            className="text-slate-400 underline font-semibold hover:text-slate-200 cursor-pointer transition duration-200 ease-in-out",
                        )
                    ],
                    className="text-slate-400 text-lg select-none",
                )
    elif is_trading_flag:
        run_trading_cycle()
        return update_log(), CLIENT_CONFIG.current_balance, CLIENT_CONFIG.current_balance - CLIENT_CONFIG.initial_balance, html.P(
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
                "..."
            ],
            className="animate-pulse text-slate-400 text-lg select-none",
        )
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



if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0")