from dash import Dash, html, dcc, callback, Output, Input, ctx, State
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
from configs.server_conf import logger
import dash_echarts as dec
from services.strategy_utils import run_strategy, fetch_data
from services.risk_manager import fetch_trade_markers
from components.common.wrappers import paperWrapperComponent
from components.tables import *
from datetime import datetime as dt
import plotly.graph_objs as go
from textwrap import dedent
from dash_iconify import DashIconify
from data.store import results_df, trades_df, full_trade_df


def drawer():
    return dmc.Drawer(
        [
            #! TODO add client overview (remaining balance, etc.)
            #! TODO add terminal monitor
            #! TODO add other params in main.py
            # four rows for four divs, flex. each div contains a backtestConfigTableComponent
            html.Div(
                [
                    oandaClientConfigTableComponent(),
                ],
                className="flex-1",
            ),
            html.Div(
                [
                    tradeConfigTableComponent(),
                ],
                className="flex-1",
            ),
            html.Div(
                [
                    tradeSecondaryConfigTableComponent(),
                ],
                className="flex-1",
            ),
            html.Div(
                [
                    backendTerminalMonitorTableComponent(),
                ],
                className="flex-1",
            ),
        ],
        title="CONFIGURATION",
        id="dashboard-page-drawer",
        padding="md",
        size="33%",
        zIndex=1000,
        overlayOpacity=0.2,
        position="top",
        classNames={"drawer": "bg-slate-800 text-slate-300 overflow-hidden flex flex-col", "body": "flex flex-row flex-1 overflow-hidden justify-between items-stretch", "header":"mb-0"},
    )


def dashboardPage():
    # Assuming 'results_df' is your DataFrame and has been defined previously.

    # Extract the data for plotting to ensure alignment
    dates = results_df.iloc[::200]["Date"]
    cumulative_portfolio_returns = results_df.iloc[::200][
        "cumulative_portfolio_returns"
    ]
    cumulative_portfolio_strategy = results_df.iloc[::200][
        "cumulative_portfolio_strategy"
    ]

    # Define the offset for adjacent bars within the same group
    offset = 0.5 * (
        dates.shape[0] - 1
    )  # Adjust this value as needed for your visual preference

    # Generate x-coordinates for the bars
    x_values = np.arange(len(dates))

    # Create the base figure
    cumReturnBarFig = go.Figure()

    # Add the first bar trace for cumulative_portfolio_returns
    cumReturnBarFig.add_trace(
        go.Bar(
            x=x_values - offset,
            y=cumulative_portfolio_returns,
            name="Benchmark",
            marker_color="rgb(16, 185, 129)",
        )
    )

    # Add the second bar trace for cumulative_portfolio_strategy
    cumReturnBarFig.add_trace(
        go.Bar(
            x=x_values + offset,
            y=cumulative_portfolio_strategy,
            name="Strategy",
            marker_color="rgb(244, 63, 94)",
        )
    )

    # Update the layout to group bars and set the x-axis with date labels
    cumReturnBarFig.update_layout(
        autosize=True,
        margin=dict(l=0, r=20, t=10, b=0),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="rgb(100,116,139)"),
        barmode="overlay",
        xaxis={"showticklabels": False, "title": "Date"},
        yaxis={
            "title": "Cumulative Returns",
            "gridcolor": "rgb(148, 163, 184)",
            "zerolinecolor": "rgb(148, 163, 184)",
        },
        showlegend=False,
    )

    drawDownFig = go.Figure()
    drawDownFig.add_trace(
        go.Scatter(
            x=results_df["Date"],
            y=results_df["cum_max"],
            mode="lines",
            name="cum_max",
            line=dict(color="rgb(16, 185, 129)"),
        )
    )
    drawDownFig.add_trace(
        go.Scatter(
            x=results_df["Date"],
            y=results_df["cumulative_portfolio_strategy"],
            mode="lines",
            name="Return",
            line=dict(color="rgb(244, 63, 94)"),
        )
    )

    drawDownFig.update_layout(
        autosize=True,
        margin=dict(l=0, r=20, t=10, b=0),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="rgb(100,116,139)"),
        xaxis={"showticklabels": False, "title": "Date", "showgrid": False},
        yaxis={
            "title": "Drawdown",
            "showgrid": False,
            "zerolinecolor": "rgb(148, 163, 184)",
        },
        showlegend=False,
    )
    # rolling sharpe ratio
    rollingSharpeFig = go.Figure()
    results_df["rolling_sharpe_strategy"] = (
        results_df["portfolio_strategy"].rolling(window=21).mean()
        / results_df["portfolio_strategy"].rolling(window=21).std()
    )
    results_df["rolling_sharpe_returns"] = (
        results_df["portfolio_returns"].rolling(window=21).mean()
        / results_df["portfolio_returns"].rolling(window=21).std()
    )
    rollingSharpeFig.add_trace(
        go.Scatter(
            x=results_df["Date"],
            y=results_df["rolling_sharpe_returns"],
            mode="lines",
            name="Benchmark",
            line=dict(color="rgb(16, 185, 129)"),
        )
    )
    rollingSharpeFig.add_trace(
        go.Scatter(
            x=results_df["Date"],
            y=results_df["rolling_sharpe_strategy"],
            mode="lines",
            name="Strategy",
            line=dict(color="rgb(244, 63, 94)"),
        )
    )
    rollingSharpeFig.update_layout(
        autosize=True,
        margin=dict(l=0, r=20, t=10, b=0),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="rgb(100,116,139)"),
        xaxis={
            "showticklabels": False,
            "title": "Date",
            "showgrid": False,
        },
        yaxis={
            "title": "Rolling Sharpe Ratio",
            "showgrid": False,
            "zerolinecolor": "rgb(148, 163, 184)",
        },
        showlegend=False,
    )
    ticker_records = fetch_data(TRADE_CONFIG.instrument, TRADE_CONFIG.lookback_count)
    stock_full_trade_df = full_trade_df[full_trade_df["Stock"] == "AAPL"]
    # filter the row which has Stock='AAPL'
    # trade_df = full_trade_df[full_trade_df["Stock"] == "AAPL"]
    # Loop through the DataFrame and create markers
    stock_marker_df = trades_df[trades_df["Stock"] == "AAPL"]
    markers = fetch_trade_markers(last_transaction_id=800)
    shortTermMomentumRecords = []
    longTermMomentumRecords = []
    HurstRecords = []
    RSIRecords = []
    for _, row in stock_full_trade_df.iterrows():
        date = row["Date"].split(" ")[0]
        shortTermMomentumRecords.append(
            {"time": date, "value": row["ShortTermMomentum"]}
        )
        longTermMomentumRecords.append({"time": date, "value": row["LongTermMomentum"]})
        HurstRecords.append({"time": date, "value": row["Hurst"]})
        # RSIRecords.append({'time':date, 'value':row['RSI']})
    #logger.info(ticker_records[:3])
    #logger.info(shortTermMomentumRecords[:3])
    #logger.info(markers[:3])
    return html.Div(
        [
            drawer(),
            html.Button(
                [DashIconify(icon="mdi:chevron-down", width=35, height=35)],
                className="absolute top-0 left-1/2 z-[999] text-slate-500 bg-slate-800 w-[60px] h-[30px] rounded-bl-full flex items-center justify-center rounded-br-full -translate-x-1/2 shadow-md shadow-slate-950 hover:scale-[115%] hover:bg-slate-700 transition-all duration-200 ease-in-out",
                id="dashboard-page-drawer-btn",
            ),
            html.Div(
                [
                    paperWrapperComponent(
                        html.Div(
                            [
                                # three buttons, flex row, centered
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                html.P(
                                                    [
                                                        "Ready to trade...",
                                                    ],
                                                    className="text-slate-400 text-lg select-none",
                                                ),
                                            ],
                                            id="dashboard-page-trade-title",
                                            className="flex flex-col justify-start rounded-t-lg p-2 bg-slate-700 items-start w-full",
                                        ),
                                        realtimePrimaryStatsTableComponent(),
                                        html.Div(
                                            [
                                                dcc.Interval(
                                                    id="dashboard-page-trade-interval",
                                                    interval=5 * 1000,
                                                    n_intervals=0,
                                                    ),
                                                dmc.Button(
                                                    "START",
                                                    id="dashboard-page-start-trade-btn",
                                                    leftIcon=DashIconify(icon="mdi:play", width=20),
                                                    className="self-center font-semibold text-emerald-600 w-full p-2 text-center bg-transparent",
                                                    variant='white'
                                                ),
                                                dmc.Button(
                                                    "PAUSE",
                                                    id="dashboard-page-pause-trade-btn",
                                                    leftIcon=DashIconify(icon="mdi:pause", width=20),
                                                    className="self-center font-semibold text-yellow-600 w-full p-2 text-center bg-transparent",
                                                    variant='white'
                                                ),
                                                dmc.Button(
                                                    "KILL",
                                                    id="dashboard-page-kill-trade-btn",
                                                    leftIcon=DashIconify(icon="mdi:book-cancel", width=20),
                                                    className="self-center font-semibold text-rose-600 w-full p-2 text-center bg-transparent",
                                                    variant='white'
                                                ),
                                            ],
                                            className="flex flex-row justify-between items-center w-full p-2",
                                        ),
                                    ],
                                    className="h-full w-full flex flex-col justify-between items-start",
                                ),
                            ],
                            className="relative w-full h-full",
                        )
                    ),
                ],
                className="row-span-1 col-span-1 flex justify-center items-center",
            ),
            html.Div(
                [
                    paperWrapperComponent(
                        html.Div(
                            [
                                benchmarkStatsTableComponent()
                            ],
                            className="w-full h-full justify-center items-center p-2 scrollableY",
                        ),
                    ),
                ],
                className="row-span-1 col-span-1 flex justify-center items-center",
            ),
            html.Div(
                [
                    paperWrapperComponent(
                        dag.AgGrid(
                            id="infinite-grid-trade",
                            className="ag-theme-alpine pl-1",
                            columnSize="sizeToFit",
                            columnDefs=[
                                {"field": col, "cellClass": "text-slate-400 text-xs"}
                                for col in trades_df.columns
                            ],
                            defaultColDef={"sortable": True},
                            # getRowStyle={
                            #    "styleConditions":[
                            #    {
                            #        "condition":"params.data.Action == 'Buy'",
                            #        "style": {"textColor":"rgb(34 197 94)"}
                            #    },
                            #    {
                            #        "condition":"params.data.Action == 'Sell'",
                            #        "style": {"textColor":"rgb(239 68 68)"}
                            #    }
                            #    ],
                            #    "defaultStyle": {"textColor":"white"},
                            # },
                            rowModelType="infinite",
                            dashGridOptions={
                                # The number of rows rendered outside the viewable area the grid renders.
                                "rowBuffer": 10,
                                # How many blocks to keep in the store. Default is no limit, so every requested block is kept.
                                "maxBlocksInCache": 1,
                                # "rowSelection": "multiple",
                                #'suppressHorizontalScroll':True,
                            },
                        )
                    ),
                    html.Div(id="infinite-output-trade", style={"display": "none"}),
                ],
                className="row-span-1 col-span-1 flex justify-center items-center",
            ),
            html.Div(
                [
                    paperWrapperComponent(
                        # visualise 'cumulative_portfolio_returns' and 'cumulative_portfolio_strategy' in a line chart
                        dcc.Graph(
                            id="cumReturnBar-chart",
                            figure=cumReturnBarFig,
                            responsive=True,
                            config={"displayModeBar": False},
                            style={"width": "100%", "height": "100%"},
                            className="text-slate-500",
                        )
                    )
                ],
                className="row-span-1 col-span-1 flex justify-center items-center",
            ),
            html.Div(
                [
                    dcc.Interval(
                        id="dashboard-page-candlestick-chart-interval",
                        interval=5 * 1000,
                        n_intervals=0,
                    ),
                    paperWrapperComponent(
                        dash_tvlwc.Tvlwc(
                            id="dashboard-page-candlestick-chart",
                            seriesData=[
                                ticker_records,
                                # shortTermMomentumRecords,
                                # longTermMomentumRecords,
                                # HurstRecords,
                                # RSIRecords,
                            ],
                            seriesTypes=[
                                "candlestick",
                                # "line",
                                # "line",
                                # "line",
                            ],
                            seriesOptions=[
                                {
                                    # "priceLineVisible": False,
                                    # "LineSeriesOptions": {"lastPriceAnimation": 1},
                                },
                                # {"lineWidth": 1, "color": "#22c55e"},
                                # {"lineWidth": 1, "color": "#ef4444"},
                                # {"lineWidth": 1, "color": "#f59e0b"},
                            ],
                            seriesMarkers=[markers],
                            chartOptions={
                                "layout": {
                                    "background": {"type": "solid", "color": "#0f172a"},
                                    "textColor": "white",
                                },
                                "grid": {
                                    "vertLines": {"visible": False},
                                    "horzLines": {"visible": False},
                                },
                                "timeScale": {
                                    "fixLeftEdge": True,
                                    "fixRightEdge": True,
                                    "timeVisible": True,
                                    "secondsVisible": True,
                                },
                                "localization": {"locale": "en-SG"},
                            },
                            width="75dvw",
                            height="66dvh",
                        )
                    ),
                ],
                className="row-span-2 col-span-3 flex justify-center items-center",
            ),
            html.Div(
                [
                    paperWrapperComponent(
                        # visualise 'cumulative_portfolio_returns' and 'cumulative_portfolio_strategy' in a line chart
                        dcc.Graph(
                            id="drawdown-chart",
                            figure=drawDownFig,
                            responsive=True,
                            config={"displayModeBar": False},
                            style={"width": "100%", "height": "100%"},
                            className="text-slate-500",
                        )
                    )
                ],
                className="row-span-1 col-span-1 flex justify-center items-center",
            ),
            html.Div(
                [
                    paperWrapperComponent(
                        # visualise 'cumulative_portfolio_returns' and 'cumulative_portfolio_strategy' in a line chart
                        dcc.Graph(
                            id="rolling-sharpe-chart",
                            figure=rollingSharpeFig,
                            responsive=True,
                            config={"displayModeBar": False},
                            style={"width": "100%", "height": "100%"},
                            className="text-slate-500",
                        )
                    )
                ],
                className="row-span-1 col-span-1 flex justify-center items-center",
            ),
        ],
        id="dashboard-page-container",
        className="w-dvw h-dvh grid grid-cols-4 gap-2 p-2 grid-rows-3 overflow-hidden animate-slide-in-x animate-700",  #! to hide the scrollbar
    )
