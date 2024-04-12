from dash import html, dcc
import dash_ag_grid as dag
from configs.server_conf import logger
from dash_iconify import DashIconify
import dash_mantine_components as dmc
from datetime import datetime as dt
from data.store import transactions_df
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
    if id == "infinite-grid-transactions":
        columnDefs = [{"field": col} for col in transactions_df.columns]
        rowModelType = "clientSide"
        dashGridOptions = {}
    else:
        #logger.error("Invalid id for dmcTableComponent", id)
        raise ValueError("Invalid id for dmcTableComponent")
    AgGridConfig = {
        "id": id,
        "columnSize": "responsiveSizeToFit" if id=="infinite-grid-transactions" else "auto",
        "className": "ag-theme-alpine",
        "columnDefs": columnDefs,
        "defaultColDef": {"sortable": True},
        "rowModelType": rowModelType,
        "dashGridOptions": dashGridOptions,
    }
    if id == "infinite-grid-transactions":
        AgGridConfig["rowData"] = transactions_df.to_dict("records")
        return html.Div(
            [
                dag.AgGrid(style={"width": "100%", "height": "100%"}, **AgGridConfig),
            ],
            className="w-full h-full",
        )
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
                                    "Current Balance",
                                    className="font-semibold select-none pl-2",
                                ),
                                html.Td(
                                    CLIENT_CONFIG.current_balance,
                                    id="primary-stats-table-current-balance",
                                    className="text-slate-400 pr-2",
                                ),
                            ],
                            className="border-b border-slate-700",
                        ),
                        html.Tr(
                            [
                                html.Td(
                                    "Current PnL",
                                    className="font-semibold select-none pl-2",
                                ),
                                html.Td(
                                    0,
                                    id="primary-stats-table-current-pnl",
                                    className="text-slate-400 pr-2",
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
                                    0,
                                    id="primary-stats-table-pending-trades",
                                    className="text-slate-400 pr-2",
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

def openPositionStatsTableComponent():
    return html.Table(
                                    [
                                        html.Tbody(
                                            [
                                                html.Tr(
                                                    [
                                                        html.Th(),
                                                        html.Th(
                                                            "Long",
                                                            className="font-semibold text-start w-1/4 lg:w-1/3",
                                                        ),
                                                        html.Th(
                                                            "Short",
                                                            className="font-semibold text-start w-1/4 lg:w-1/3",
                                                        ),
                                                    ],
                                                    className="border-b border-slate-700",
                                                ),
                                                html.Tr(
                                                    [
                                                        html.Td(
                                                            "Units",
                                                            className="font-semibold select-none",
                                                        ),
                                                        html.Td(
                                                            0,
                                                            id="open-position-stats-table-long-units",
                                                            className="text-slate-500"
                                                        ),
                                                        html.Td(
                                                            0,
                                                            id="open-position-stats-table-short-units",
                                                            className="text-slate-500"
                                                        ),
                                                    ],
                                                    className="border-b border-slate-700",
                                                ),
                                                html.Tr(
                                                    [
                                                        html.Td(
                                                            "Avg Price",
                                                            className="font-semibold select-none",
                                                        ),
                                                        html.Td(
                                                            0,
                                                            id="open-position-stats-table-long-avg-price",
                                                            className="text-slate-500"
                                                        ),
                                                        html.Td(
                                                            0,
                                                            id="open-position-stats-table-short-avg-price",
                                                            className="text-slate-500"
                                                        ),
                                                    ],
                                                    className="border-b border-slate-700",
                                                ),
                                                html.Tr(
                                                    [
                                                        html.Td(
                                                            "Unrealized PnL",
                                                            className="font-semibold select-none",
                                                        ),
                                                        html.Td(
                                                            0,
                                                            id="open-position-stats-table-long-unrealized-pnl",
                                                            className="text-slate-500"
                                                        ),
                                                        html.Td(
                                                            0,
                                                            id="open-position-stats-table-short-unrealized-pnl",
                                                            className="text-slate-500"
                                                        ),
                                                    ],
                                                ),
                                                html.Tr(
                                                    [
                                                        html.Td(
                                                            "Margin Used",
                                                            className="font-semibold select-none",
                                                        ),
                                                        html.Td(
                                                            0,
                                                            id="open-position-stats-table-long-margin-used",
                                                            className="text-slate-500"
                                                        ),
                                                        html.Td(
                                                            0,
                                                            id="open-position-stats-table-short-margin-used",
                                                            className="text-slate-500"
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
                                            dcc.Input(debounce=True,
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
                                            dcc.Input(debounce=True,
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
                                            dcc.Input(debounce=True,
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
                                            dcc.Input(debounce=True,
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

def tradeConfigTableComponent():
    return html.Div(
            [
                html.Table(
                    [
                        html.Tbody(
                            [
                                html.Tr(
                                    [
                                        html.Td(
                                            "Instrument",
                                            className="font-semibold select-none",
                                        ),
                                        html.Td(
                                            dcc.Input(debounce=True,
                                                id="trade-instrument-input",
                                                type="text",
                                                value=TRADE_CONFIG.instrument,
                                                className="underline underline-offset-2 w-full rounded-md text-slate-500 bg-slate-800 text-sm hover:text-slate-400 focus:text-slate-400 transition duration-300 ease-in-out",
                                            )
                                        ),
                                    ],
                                    className="border-b border-slate-700",
                                ),
                                html.Tr(
                                    [
                                        html.Td(
                                            "Lookback Count",
                                            className="font-semibold select-none",
                                        ),
                                        html.Td(
                                            dcc.Input(debounce=True,
                                                id="trade-lookback-count-input",
                                                type="text",
                                                value=TRADE_CONFIG.lookback_count,
                                                className="underline underline-offset-2 w-full rounded-md text-slate-500 bg-slate-800 text-sm hover:text-slate-400 focus:text-slate-400 transition duration-300 ease-in-out",
                                            )
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
                                            dcc.Input(debounce=True,
                                                id="trade-short-window-input",
                                                type="number",
                                                value=TRADE_CONFIG.st_period,
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
                                            dcc.Input(debounce=True,
                                                id="trade-long-window-input",
                                                type="number",
                                                value=TRADE_CONFIG.lt_period,
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
                                            dcc.Input(debounce=True,
                                                id="trade-hurst-window-input",
                                                type="number",
                                                value=TRADE_CONFIG.hurst_period,
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
def tradeSecondaryConfigTableComponent():
    return html.Div(
            [
                html.Table(
                    [
                        html.Tbody(
                            [
                                html.Tr(
                                    [
                                        html.Td(
                                            "Risk Factor",
                                            className="font-semibold select-none",
                                        ),
                                        html.Td(
                                            dcc.Input(debounce=True,
                                                id="trade-risk-factor-input",
                                                type="text",
                                                value=TRADE_CONFIG.risk_factor,
                                                className="underline underline-offset-2 w-full rounded-md text-slate-500 bg-slate-800 text-sm hover:text-slate-400 focus:text-slate-400 transition duration-300 ease-in-out",
                                            )
                                        ),
                                    ],
                                    className="border-b border-slate-700",
                                ),
                                html.Tr(
                                    [
                                        html.Td(
                                            "Risk Reward",
                                            className="font-semibold select-none",
                                        ),
                                        html.Td(
                                            dcc.Input(debounce=True,
                                                id="trade-risk-reward-input",
                                                type="text",
                                                value=TRADE_CONFIG.risk_reward,
                                                className="underline underline-offset-2 w-full rounded-md text-slate-500 bg-slate-800 text-sm hover:text-slate-400 focus:text-slate-400 transition duration-300 ease-in-out",
                                            )
                                        ),
                                    ],
                                    className="border-b border-slate-700",
                                ),
                                html.Tr(
                                    [
                                        html.Td(
                                            "Granularity",
                                            className="font-semibold select-none",
                                        ),
                                        html.Td(
                                            dcc.Input(debounce=True,
                                                id="trade-granularity-input",
                                                type="text",
                                                value=TRADE_CONFIG.granularity,
                                                className="underline underline-offset-2 w-full rounded-md text-slate-500 bg-slate-800 text-sm hover:text-slate-400 focus:text-slate-400 transition duration-300 ease-in-out",
                                            )
                                        ),
                                    ],
                                    className="border-b border-slate-700",
                                ),
                                html.Tr(
                                    [
                                        html.Td(
                                            "Stoploss PnL",
                                            className="font-semibold select-none",
                                        ),
                                        html.Td(
                                            dcc.Input(debounce=True,
                                                id="trade-stoploss-pnl-input",
                                                type="number",
                                                disabled=True,
                                                value=CLIENT_CONFIG.initial_balance * TRADE_CONFIG.risk_factor,
                                                className="underline underline-offset-2 w-full rounded-md text-slate-500 bg-slate-800 text-sm hover:text-slate-400 focus:text-slate-400 transition duration-300 ease-in-out",
                                            )
                                        ),
                                    ],
                                    className="border-b border-slate-700",
                                ),
                                html.Tr(
                                    [
                                        html.Td(
                                            "Target PnL",
                                            className="font-semibold select-none",
                                        ),
                                        html.Td(
                                            dcc.Input(debounce=True,
                                                id="trade-target-pnl-input",
                                                type="number",
                                                disabled=True,
                                                value=CLIENT_CONFIG.initial_balance * TRADE_CONFIG.risk_factor * TRADE_CONFIG.risk_reward,
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
                                            dcc.Input(debounce=True,
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
                                            dcc.Input(debounce=True,
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
                                            dcc.Input(debounce=True,
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
                                            "Initial Balance",
                                            className="font-semibold select-none",
                                        ),
                                        html.Td(
                                            html.Div(CLIENT_CONFIG.initial_balance, id="oanda-account-balance", className="text-emerald-500 pr-2"),
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

def readlog():
    # read last 100 lines of the log file & return as html.P for each line
    with open("app.log", "r") as f:
        lines = f.readlines()[-100:]
        #sort the lines in reverse order
        lines.reverse()
    return html.Div([html.P(line) for line in lines], className="w-full h-full scrollableY")
def backendTerminalMonitorTableComponent():

    return html.Div(
        [
            html.Div([
            DashIconify(icon="mdi:terminal", className="text-slate-400 text-2xl"),
            html.P("Terminal", className="font-semibold text-slate-400 text-lg"),
                ], className="w-full flex flex-row justify-start gap-2 items-center"),
            html.Div(readlog(), id="dashboard-page-log",className="flex-1 bg-slate-900 h-full font-consolas p-2 rounded-lg"),
        ],
        className="w-full h-full justify-center items-center p-1",
    )
# def format_percentage_difference(column_name):
#     # Ensure that the DataFrame contains the column and the necessary index labels
#     if (
#         column_name in metrics_df.columns
#         and "Portfolio Returns" in metrics_df.index
#         and "Portfolio Strategy" in metrics_df.index
#     ):

#         # Fetch the values for "Portfolio Returns" and "Portfolio Strategy"
#         portfolio_returns_value = metrics_df.loc["Portfolio Returns", column_name]
#         portfolio_strategy_value = metrics_df.loc["Portfolio Strategy", column_name]

#         # Calculate the percentage difference
#         if portfolio_returns_value != 0:
#             percentage_diff = (
#                 portfolio_strategy_value - portfolio_returns_value
#             ) / abs(portfolio_returns_value)
#             # Format the string with a plus or minus sign based on the difference
#             return (
#                 f"({'+' if percentage_diff >= 0 else '-' }{abs(percentage_diff):.2%})"
#             )
#         else:
#             # Handle the case where the denominator is zero
#             return "(N/A)"  # or some other placeholder text
#     else:
#         raise ValueError("Invalid column name or missing index labels in DataFrame.")
