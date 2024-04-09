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
from components.common.wrappers import paperWrapperComponent
from datetime import datetime as dt
import plotly.graph_objs as go
from textwrap import dedent
from configs.server_conf import logger, app
from pages.landing_page import landingPage
from pages.dashboard_page import dashboardPage
from pages.analysis_page import analysisInitialPage, analysisDetailPage
from components.tables import dmcTableComponent
from components.figures import visualisationFiguresGrid
from data.store import trades_df, full_trade_df
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
    return [fetch_data('EUR_USD', 200)]

@app.callback(
    Output("dashboard-page-candlestick-chart", "seriesData"),
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
def update_dashboard_page_candlestick(
    *args#seriesData: list[list[dict]], nIntervals: int, data: dict[list], *args
) -> list[list[dict]]:
    """Update the candlestick chart on the landing page. Either by clicking on the navbar or by the interval dynamic update.

    Args:
        seriesData (list[list[dict]]): series data of tmvlwc.
        nIntervals (int): number of interval.

    Returns:
        list[list[dict]]: updated series data.
    """
    return [fetch_data('EUR_USD', 500)]

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
    logger.info("Erase title and replace with analysis page layout.")
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
        logger.info("Switch to dashboard page.")
        return dashboardPage()
    if pathname == "/analysis":
        # deal with delay by client side js
        # ////time.sleep(0.2)  #! hack way to wait for the transition to finish
        logger.info("Switch to analysis page.")
        return analysisInitialPage()
    logger.info(f"Switch to landing page for {pathname}.")
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