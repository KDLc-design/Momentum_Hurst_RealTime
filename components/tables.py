from dash import html, dcc
import dash_ag_grid as dag
from configs.server_conf import logger
import dash_mantine_components as dmc
from datetime import datetime as dt
from data.store import full_trade_df, trades_df, metrics_df, results_df
from configs.oanda_conf import CLIENT_CONFIG, TRADE_CONFIG
def dmcTableComponent(id):
    rowModelType = "infinite"
    dashGridOptions = {
        # The number of rows rendered outside the viewable area the grid renders.
        "rowBuffer": 10,
        # How many blocks to keep in the store. Default is no limit, so every requested block is kept.
        "maxBlocksInCache": 1,
        "rowSelection": "multiple",
    }
    if id == "analysis-page-infinite-grid-full-trades":
        columnDefs = [{"field": col} for col in full_trade_df.columns]
    elif id == "infinite-grid-trade":
        columnDefs = [{"field": col} for col in trades_df.columns]
    elif id == "analysis-page-infinite-grid-metrics":
        columnDefs = [{"field": col} for col in metrics_df.columns]
        rowModelType = "clientSide"
        dashGridOptions = {}
    elif id == "analysis-page-infinite-grid-results":
        columnDefs = [{"field": col} for col in results_df.columns]
    else:
        logger.error("Invalid id for dmcTableComponent", id)
        raise ValueError("Invalid id for dmcTableComponent")
    AgGridConfig = {
        "id": id,
        "columnSize": "sizeToFit",
        "className": "ag-theme-alpine",
        "columnDefs": columnDefs,
        "defaultColDef": {"sortable": True},
        "rowModelType": rowModelType,
        "dashGridOptions": dashGridOptions,
    }
    if id == "analysis-page-infinite-grid-metrics":
        AgGridConfig["rowData"] = metrics_df.to_dict("records")
    return html.Div(
        [
            dag.AgGrid(style={"width": "100%", "height": "100%"}, **AgGridConfig),
            html.Div(id=f"{id}-infinite-output"),
        ],
        className="w-full h-full animate-fade-in animate-400",
    )


def realtimePrimaryStatsTableComponent():
    return html.Table(
            [
                html.Tbody(
                    [
                        html.Tr(
                            [
                                html.Td(
                                    "Current Profit/Loss",
                                    className="font-semibold select-none pl-2",
                                ),
                                html.Td(
                                    "$0.00",
                                    className="text-emerald-600 pr-2",
                                ),
                            ],
                            className="border-b border-slate-700",
                        ),
                        html.Tr(
                            [
                                html.Td(
                                    "Pending Trades",
                                    className="font-semibold select-none pl-2",
                                ),
                                html.Td(
                                    "10",
                                    className="text-emerald-600 pr-2",
                                ),
                            ],
                            className="border-b border-slate-700",
                        ),
                        html.Tr(
                            [
                                html.Td(
                                    "Fulfilled Trades",
                                    className="font-semibold select-none pl-2",
                                ),
                                html.Td(
                                    "100",
                                    className="text-emerald-600 pr-2",
                                ),
                            ],
                            className="border-b border-slate-700",
                        ),
                    ],
                    className="w-full h-full text-slate-400",
                ),
            ],
            className="w-full h-full",
        )

def benchmarkStatsTableComponent():
    return html.Table(
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


def backtestConfigTableComponent():
    return html.Div(
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
                                                value=dt(2015, 1, 1),
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
                                                value=dt(2019, 12, 31),
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
        )

def oandaClientConfigTableComponent():
    return html.Div(
            [
                html.Table(
                    [
                        html.Tbody(
                            [
                                html.Tr(
                                    [
                                        html.Td(
                                            "API Provider",
                                            className="font-semibold select-none",
                                        ),
                                        html.Td(
                                            "Oanda",
                                            className="text-slate-400 pr-2",
                                        ),
                                    ],
                                    className="border-b border-slate-700",
                                ),
                                html.Tr(
                                    [
                                        html.Td(
                                            "Access Token",
                                            className="font-semibold select-none",
                                        ),
                                        html.Td(
                                            dcc.Input(
                                                id="oanda-access-token-input",
                                                type="text",
                                                value=CLIENT_CONFIG.access_token,
                                                className="underline underline-offset-2 w-full rounded-md text-slate-500 bg-slate-800 text-sm hover:text-slate-400 focus:text-slate-400 transition duration-300 ease-in-out",
                                            )
                                        ),
                                    ],
                                    className="border-b border-slate-700",
                                ),
                                html.Tr(
                                    [
                                        html.Td(
                                            "Accound ID",
                                            className="font-semibold select-none",
                                        ),
                                        html.Td(
                                            dcc.Input(
                                                id="oanda-account-id-input",
                                                type="text",
                                                value=CLIENT_CONFIG.account_id,
                                                className="underline underline-offset-2 w-full rounded-md text-slate-500 bg-slate-800 text-sm hover:text-slate-400 focus:text-slate-400 transition duration-300 ease-in-out",
                                            )
                                        ),
                                    ],
                                    className="border-b border-slate-700",
                                ),
                                html.Tr(
                                    [
                                        html.Td(
                                            "Environment",
                                            className="font-semibold select-none",
                                        ),
                                        html.Td(
                                            dcc.Input(
                                                id="oanda-account-environment-input",
                                                type="text",
                                                value=CLIENT_CONFIG.environment,
                                                className="underline underline-offset-2 w-full rounded-md text-slate-500 bg-slate-800 text-sm hover:text-slate-400 focus:text-slate-400 transition duration-300 ease-in-out",
                                            )
                                        ),
                                    ],
                                    className="border-b border-slate-700",
                                ),
                                html.Tr(
                                    [
                                        html.Td(
                                            "Connect API",
                                            className="font-semibold select-none",
                                        ),
                                        html.Td(
                                            html.Button(
                                                "Connected",
                                                id="connect-oanda-api-btn",
                                                className="text-md font-semibold text-slate-50 bg-emerald-500 px-3 py-1 rounded-lg hover:bg-emerald-600 transition duration-300 ease-in-out",
                                            )
                                        ),
                                    ],
                                    className="border-b border-slate-700",
                                ),
                            ],
                            className="w-full h-full text-slate-400",
                        ),
                    ],
                    className="w-full h-full",
                )
            ],
            className="w-full h-full justify-center items-center p-1 scrollableY",
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
