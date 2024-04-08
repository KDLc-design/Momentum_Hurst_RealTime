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
from configs.server_conf import logger, results_df, metrics_df, trades_df, full_trade_df
import dash_echarts as dec
from services.strategy_utils import run_strategy, fetch_data
from components.common.wrappers import paperWrapperComponent
from datetime import datetime as dt
import plotly.graph_objs as go
from textwrap import dedent

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
    ticker_records = fetch_data('EUR_USD', 500)
    stock_full_trade_df = full_trade_df[full_trade_df["Stock"] == "AAPL"]
    # filter the row which has Stock='AAPL'
    # trade_df = full_trade_df[full_trade_df["Stock"] == "AAPL"]
    # Loop through the DataFrame and create markers
    stock_marker_df = trades_df[trades_df["Stock"] == "AAPL"]
    markers = []
    for _, row in stock_marker_df.iterrows():
        marker = {
            "time": dt.strptime(row["Date"], "%d/%m/%y").strftime(
                "%Y-%m-%d"
            ),  # Format the time in a way that's compatible with your charting library
            "position": "aboveBar" if row["Action"] == "Sell" else "belowBar",
            "color": (
                "rgb(244, 63, 94)" if row["Action"] == "Sell" else "rgb(16, 185, 129)"
            ),
            "shape": "arrowDown" if row["Action"] == "Sell" else "arrowUp",
            "text": row["Action"],
        }
        markers.append(marker)
    # sort the markers by time
    markers.reverse()
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
    logger.info(ticker_records[:3])
    logger.info(shortTermMomentumRecords[:3])
    logger.info(markers[:3])
    return html.Div(
        [
            html.Div(
                [
                    paperWrapperComponent(
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.Table(
                                            [
                                                html.Tbody(
                                                    [
                                                        html.Tr(
                                                            [
                                                                html.Td(
                                                                    "Tickers",
                                                                    className="font-semibold select-none",
                                                                ),
                                                                html.Td(
                                                                    dcc.Input(
                                                                        id="stocks-input",
                                                                        type="text",
                                                                        value="AAPL, GOOGL, NFLX, AMZN, META",
                                                                        className="underline underline-offset-2 w-full rounded-md text-slate-500 bg-slate-800 text-sm hover:text-slate-400 focus:text-slate-400 transition duration-300 ease-in-out",
                                                                    )
                                                                ),
                                                            ],
                                                            className="border-b border-slate-700",
                                                        ),
                                                        html.Tr(
                                                            [
                                                                html.Td(
                                                                    "Start Date",
                                                                    className="font-semibold select-none",
                                                                ),
                                                                html.Td(
                                                                    dmc.DatePicker(
                                                                        id="start-date-picker",
                                                                        placeholder="Pick a start date...",
                                                                        value=dt(
                                                                            2015, 1, 1
                                                                        ),
                                                                        size="xs",
                                                                        classNames={
                                                                            "input": "border-0 text-slate-500 bg-slate-800 underline underline-offset-2 text-sm p-0 hover:text-slate-400 transition duration-300 ease-in-out",
                                                                            "dropdown": " border-slate-700 bg-slate-800",
                                                                        },
                                                                        className="font-urbanist text-slate-400",
                                                                    ),
                                                                ),
                                                            ],
                                                            className="border-b border-slate-700",
                                                        ),
                                                        html.Tr(
                                                            [
                                                                html.Td(
                                                                    "End Date",
                                                                    className="font-semibold select-none",
                                                                ),
                                                                html.Td(
                                                                    dmc.DatePicker(
                                                                        id="end-date-picker",
                                                                        placeholder="Pick an end date...",
                                                                        value=dt(
                                                                            2019, 12, 31
                                                                        ),
                                                                        size="xs",
                                                                        classNames={
                                                                            "input": "border-0 text-slate-500 bg-slate-800 underline underline-offset-2 text-sm p-0 hover:text-slate-400 transition duration-300 ease-in-out",
                                                                            "dropdown": " border-slate-700 bg-slate-800",
                                                                        },
                                                                        className="font-urbanist text-slate-400",
                                                                    ),
                                                                ),
                                                            ],
                                                            className="border-b border-slate-700",
                                                        ),
                                                        html.Tr(
                                                            [
                                                                html.Td(
                                                                    "Short Window",
                                                                    className="font-semibold select-none",
                                                                ),
                                                                html.Td(
                                                                    dcc.Input(
                                                                        id="short-window-input",
                                                                        type="number",
                                                                        value=5,
                                                                        className="underline underline-offset-2 w-full rounded-md text-slate-500 bg-slate-800 text-sm hover:text-slate-400 focus:text-slate-400 transition duration-300 ease-in-out",
                                                                    )
                                                                ),
                                                            ],
                                                            className="border-b border-slate-700",
                                                        ),
                                                        html.Tr(
                                                            [
                                                                html.Td(
                                                                    "Long Window",
                                                                    className="font-semibold select-none",
                                                                ),
                                                                html.Td(
                                                                    dcc.Input(
                                                                        id="long-window-input",
                                                                        type="number",
                                                                        value=21,
                                                                        className="underline underline-offset-2 w-full rounded-md text-slate-500 bg-slate-800 text-sm hover:text-slate-400 focus:text-slate-400 transition duration-300 ease-in-out",
                                                                    )
                                                                ),
                                                            ],
                                                            className="border-b border-slate-700",
                                                        ),
                                                        html.Tr(
                                                            [
                                                                html.Td(
                                                                    "Hurst Window",
                                                                    className="font-semibold select-none",
                                                                ),
                                                                html.Td(
                                                                    dcc.Input(
                                                                        id="hurst-window-input",
                                                                        type="number",
                                                                        value=200,
                                                                        className="underline underline-offset-2 w-full rounded-md text-slate-500 bg-slate-800 text-sm hover:text-slate-400 focus:text-slate-400 transition duration-300 ease-in-out",
                                                                    )
                                                                ),
                                                            ]
                                                        ),
                                                    ],
                                                    className="w-full h-full text-slate-400",
                                                ),
                                            ],
                                            className="w-full h-full",
                                        )
                                    ],
                                    className="w-full h-full justify-center items-center p-1 scrollableY",
                                ),
                                html.Div(
                                    [
                                        html.Button(
                                            "Back",
                                            id="demo-btn",
                                            className="w-full h-10 bg-slate-700 text-slate-200 text-xs md:text-sm lg:text-md font-semibold rounded-md hover:bg-slate-600 focus:bg-slate-600 transition duration-300 ease-in-out",
                                        )
                                    ],
                                    className="absolute bottom-2 right-4 w-[30%] h-[20%]",
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
                                html.Table(
                                    [
                                        html.Tbody(
                                            [
                                                html.Tr(
                                                    [
                                                        html.Th(),
                                                        html.Th(
                                                            "Benchmark",
                                                            className="font-semibold text-start",
                                                        ),
                                                        html.Th(
                                                            "Strategy",
                                                            className="font-semibold text-start",
                                                        ),
                                                    ],
                                                    className="border-b border-slate-700",
                                                ),
                                                # Annual Return
                                                html.Tr(
                                                    [
                                                        html.Td(
                                                            "Annual Return",
                                                            className="font-semibold select-none",
                                                        ),
                                                        # get the annual return from the metrics_df, column name is 'Annual Return', row index is "Portfolio Returns"
                                                        html.Td(
                                                            metrics_df.loc[
                                                                "Portfolio Returns",
                                                                "Annual Return",
                                                            ].round(3),
                                                            className=(
                                                                "text-emerald-500"
                                                                if metrics_df.loc[
                                                                    "Portfolio Returns",
                                                                    "Annual Return",
                                                                ].round(3)
                                                                > metrics_df.loc[
                                                                    "Portfolio Strategy",
                                                                    "Annual Return",
                                                                ].round(3)
                                                                else "text-rose-500"
                                                            ),
                                                        ),
                                                        html.Td(
                                                            f'{metrics_df.loc["Portfolio Strategy", "Annual Return"].round(3)} {format_percentage_difference("Annual Return")}',
                                                            className=(
                                                                "text-emerald-500"
                                                                if metrics_df.loc[
                                                                    "Portfolio Returns",
                                                                    "Annual Return",
                                                                ].round(3)
                                                                < metrics_df.loc[
                                                                    "Portfolio Strategy",
                                                                    "Annual Return",
                                                                ].round(3)
                                                                else "text-rose-500"
                                                            ),
                                                        ),
                                                    ],
                                                    className="border-b border-slate-700",
                                                ),
                                                # Annual Std
                                                html.Tr(
                                                    [
                                                        html.Td(
                                                            "Annual Std",
                                                            className="font-semibold select-none",
                                                        ),
                                                        # get the annual std from the metrics_df, column name is 'Annual Std', row index is "Portfolio Returns"
                                                        html.Td(
                                                            metrics_df.loc[
                                                                "Portfolio Returns",
                                                                "Annual Std",
                                                            ].round(3),
                                                            className=(
                                                                "text-emerald-500"
                                                                if metrics_df.loc[
                                                                    "Portfolio Returns",
                                                                    "Annual Std",
                                                                ].round(3)
                                                                > metrics_df.loc[
                                                                    "Portfolio Strategy",
                                                                    "Annual Std",
                                                                ].round(3)
                                                                else "text-rose-500"
                                                            ),
                                                        ),
                                                        html.Td(
                                                            f'{metrics_df.loc["Portfolio Strategy", "Annual Std"].round(3)} {format_percentage_difference("Annual Std")}',
                                                            className=(
                                                                "text-emerald-500"
                                                                if metrics_df.loc[
                                                                    "Portfolio Returns",
                                                                    "Annual Std",
                                                                ].round(3)
                                                                < metrics_df.loc[
                                                                    "Portfolio Strategy",
                                                                    "Annual Std",
                                                                ].round(3)
                                                                else "text-rose-500"
                                                            ),
                                                        ),
                                                    ],
                                                    className="border-b border-slate-700",
                                                ),
                                                # sharpe ratio
                                                html.Tr(
                                                    [
                                                        html.Td(
                                                            "Sharpe Ratio",
                                                            className="font-semibold select-none",
                                                        ),
                                                        # get the sharpe ratio from the metrics_df, column name is 'Sharpe Ratio', row index is "Portfolio Strategy"
                                                        html.Td(
                                                            metrics_df.loc[
                                                                "Portfolio Returns",
                                                                "Sharpe Ratio",
                                                            ].round(3),
                                                            className=(
                                                                "text-emerald-500"
                                                                if metrics_df.loc[
                                                                    "Portfolio Returns",
                                                                    "Sharpe Ratio",
                                                                ].round(3)
                                                                > metrics_df.loc[
                                                                    "Portfolio Strategy",
                                                                    "Sharpe Ratio",
                                                                ].round(3)
                                                                else "text-rose-500"
                                                            ),
                                                        ),
                                                        html.Td(
                                                            f'{metrics_df.loc["Portfolio Strategy", "Sharpe Ratio"].round(3)} {format_percentage_difference("Sharpe Ratio")}',
                                                            className=(
                                                                "text-emerald-500"
                                                                if metrics_df.loc[
                                                                    "Portfolio Returns",
                                                                    "Sharpe Ratio",
                                                                ].round(3)
                                                                < metrics_df.loc[
                                                                    "Portfolio Strategy",
                                                                    "Sharpe Ratio",
                                                                ].round(3)
                                                                else "text-rose-500"
                                                            ),
                                                        ),
                                                    ],
                                                ),
                                            ],
                                            className="w-full h-full text-slate-400",
                                        ),
                                    ],
                                    className="w-full h-full",
                                )
                            ],
                            className="w-full h-full justify-center items-center p-1 scrollableY",
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
                            #seriesMarkers=[markers],
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
                                "localization": {"locale": "en-US"},
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



def format_percentage_difference(column_name):
    # Ensure that the DataFrame contains the column and the necessary index labels
    if (
        column_name in metrics_df.columns
        and "Portfolio Returns" in metrics_df.index
        and "Portfolio Strategy" in metrics_df.index
    ):

        # Fetch the values for "Portfolio Returns" and "Portfolio Strategy"
        portfolio_returns_value = metrics_df.loc["Portfolio Returns", column_name]
        portfolio_strategy_value = metrics_df.loc["Portfolio Strategy", column_name]

        # Calculate the percentage difference
        if portfolio_returns_value != 0:
            percentage_diff = (
                portfolio_strategy_value - portfolio_returns_value
            ) / abs(portfolio_returns_value)
            # Format the string with a plus or minus sign based on the difference
            return (
                f"({'+' if percentage_diff >= 0 else '-' }{abs(percentage_diff):.2%})"
            )
        else:
            # Handle the case where the denominator is zero
            return "(N/A)"  # or some other placeholder text
    else:
        raise ValueError("Invalid column name or missing index labels in DataFrame.")

