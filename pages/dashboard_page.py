from dash import html, dcc
import dash_mantine_components as dmc
from dash_tvlwc import Tvlwc
from services.signal_generator import fetch_data
from services.risk_manager import fetch_trade_markers
from components.common.wrappers import paperWrapperComponent
from components.tables import *
from dash_iconify import DashIconify
from data.store import strategy_returns_list, benchmark_returns_list, indicators_lists_dict
from components.figures import create_line_chart
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
    candlestick_data = fetch_data(TRADE_CONFIG.instrument, TRADE_CONFIG.lookback_count)
    markers = fetch_trade_markers(last_transaction_id=800)
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
            # html.Div(
            #     [
            #         paperWrapperComponent(
            #             html.Div(
            #                 [
            #                     benchmarkStatsTableComponent()
            #                 ],
            #                 className="w-full h-full justify-center items-center p-2 scrollableY",
            #             ),
            #         ),
            #     ],
            #     className="row-span-1 col-span-1 flex justify-center items-center",
            # ),
            html.Div(
                [
                    paperWrapperComponent(
                        dmcTableComponent("infinite-grid-transactions")
                    )
                ],
                className="row-span-1 col-span-2 flex justify-center items-center",
            ),
            html.Div(
                [
                    paperWrapperComponent(
                        # visualise 'cumulative_portfolio_returns' and 'cumulative_portfolio_strategy' in a line chart
                        dcc.Graph(
                            id="hurst-line-fig",
                            figure=hurst_fig,
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
                        Tvlwc(
                            id="dashboard-page-candlestick-chart",
                            seriesData=[
                                candlestick_data,
                                # benchmark_returns_df,
                                #strategy_returns_df
                                # shortTermMomentumRecords,
                                # longTermMomentumRecords,
                                # HurstRecords,
                                # RSIRecords,
                            ],
                            seriesTypes=[
                                "candlestick",
                                # "line",
                                #"line",
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
                                    "borderVisible":False,
                                },
                                "localization": {"locale": "en-SG"},
                            },
                            width="74dvw",
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
                            id="momentums-line-fig",
                            figure=momentums_fig,
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
                            id="returns-comparison-line-fig",
                            figure=returns_comparison_line_fig,
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
