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
import logging
import dash_echarts as dec
from utils.strategy_utils import run_strategy, fetch_data
from datetime import datetime as dt
import plotly.graph_objs as go
from textwrap import dedent

# create a console and file logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
# create a file handler
file_handler = logging.FileHandler("app.log")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
# create a stream handler
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
stream_handler.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(stream_handler)
# call the ability to add external scripts
external_scripts = [
    # add the tailwind cdn url hosting the files with the utility classes
    {"src": "https://cdn.tailwindcss.com"}
]
results_df, metrics_df, trades_df, full_trade_df = run_strategy()

app = Dash(
    __name__, external_scripts=external_scripts, suppress_callback_exceptions=True
)

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


@callback(
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

@callback(
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

@callback(
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
    return scrollAreaComponent()


@callback(
    Output("analysis-page-infinite-grid-full-trades-container", "children"),
    Input("analysis-page-infinite-grid-full-trades-btn", "n_clicks"),
    prevent_initial_call=True,
)
def showResults(nClicks: int) -> dash_tvlwc.Tvlwc:
    if nClicks is None:
        raise PreventUpdate
    return dmcTableComponent(
        "analysis-page-infinite-grid-full-trades"
    )  # tvwlcComponent()


@callback(
    Output("analysis-page-infinite-grid-metrics-container", "children"),
    Input("analysis-page-infinite-grid-metrics-btn", "n_clicks"),
    prevent_initial_call=True,
)
def showResults(nClicks: int) -> dash_tvlwc.Tvlwc:
    if nClicks is None:
        raise PreventUpdate
    return dmcTableComponent("analysis-page-infinite-grid-metrics")  # tvwlcComponent()


def timelineNode(title, top):
    """Create a node on top-{%val} of the timeline.

    Args:
        title (str): title of the node in middle.
        top (str): percentage/px for CSS top.

    Returns:
        _type_: _description_
    """
    return html.Div(
        [
            html.Div(
                [
                    html.Div(
                        className=" w-[20px] h-[20px] md:w-8 md:h-8 border-t-[3px] border-l-[3px] border-slate-500"
                    ),
                    html.Div(
                        className="repeat-animation scroll-item-animate w-[20px] h-[20px] md:w-8 md:h-8 border-t-[3px] border-r-[3px] border-slate-500 need-animate-600 need-animate-delay-200 need-animate-slide-in-x-and-y hover:scale(1.05) hover:border-slate-400 transition duration-300 ease-in-out animate-slide-in-x-and-y animate-700 animate-delay-400"  # animate-slide-in-x-and-y animate-500 animate-delay-700
                    ),
                ],
                className="w-full flex flex-row justify-between items-start",
            ),
            html.H3(
                title,
                className="absolute top-1/2 left-1/2 text-slate-400 flex-1 font-semibold text-md md:text-3xl -rotate-45 text-center self-center select-none hover:text-slate-300 transition duration-500 ease-in-out translate-x-[-50%] translate-y-[-50%]",
            ),
            html.Div(
                [
                    html.Div(
                        className=" w-[20px] h-[20px] md:w-8 md:h-8 self-end border-b-[3px] border-r-[3px] border-slate-500"
                    ),
                ],
                className="w-full flex flex-row-reverse justify-between items-end",
            ),
        ],
        #! this container need animation at first place because it is the first item
        className=f"scroll-item-container absolute top-[{top}] left-[2rem] md:left-[5rem] w-14 h-14 md:w-28 md:h-28 lg:w-44 lg:h-44 bg-slate-900 rotate-45 translate-x-[-50%] translate-y-[-50%] flex flex-col justify-between",
    )


@callback(
    Output("analysis-page-infinite-grid-full-trades-infinite-output", "children"),
    Input("analysis-page-infinite-grid-full-trades", "selectedRows"),
)
def display_selected_car2(selectedRows):
    if selectedRows:
        return [f"You selected id {s['id']} and name {s['name']}" for s in selectedRows]
    raise PreventUpdate


@callback(
    Output("analysis-page-infinite-grid-full-trades", "getRowsResponse"),
    Input("analysis-page-infinite-grid-full-trades", "getRowsRequest"),
)
def infinite_scroll(request):
    if request is None:
        raise PreventUpdate
    # instead of original ascending order, we use descending order
    total_rows = full_trade_df.shape[0]
    partial = full_trade_df.iloc[
        total_rows - request["endRow"] : total_rows - request["startRow"]
    ][::-1]
    return {"rowData": partial.to_dict("records"), "rowCount": len(full_trade_df.index)}


@callback(
    Output("infinite-output-trade", "children"),
    Input("infinite-grid-trade", "selectedRows"),
)
def display_selected_car2(selectedRows):
    if selectedRows:
        return [f"You selected id {s['id']} and name {s['name']}" for s in selectedRows]
    raise PreventUpdate


@callback(
    Output("infinite-grid-trade", "getRowsResponse"),
    Input("infinite-grid-trade", "getRowsRequest"),
)
def infinite_scroll(request):
    if request is None:
        raise PreventUpdate
    partial = trades_df.iloc[request["startRow"] : request["endRow"]]
    return {"rowData": partial.to_dict("records"), "rowCount": len(trades_df.index)}


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


def gen_randlist(num):
    return random.sample(range(num), 7)


def echartsComponent():
    return html.Div(
        [
            dec.DashECharts(
                option={
                    "xAxis": {
                        "type": "category",
                        "data": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
                    },
                    "yAxis": {"type": "value"},
                    "tooltip": {},
                    "series": [
                        {"data": gen_randlist(200), "type": "line", "smooth": True},
                        {"data": gen_randlist(200), "type": "line", "smooth": True},
                    ],
                },
                # id='echarts',
                style={
                    "width": "25dvw",
                    "height": "25dvh",
                },
            )
        ],
        className="w-full h-full echarts-container relative",
    )


def visualisationComponentList():
    cumReturnLineFig = go.Figure()
    cumReturnLineFig.add_trace(
        go.Scatter(
            x=results_df["Date"],
            y=results_df["portfolio_returns"].cumsum(),
            mode="lines",
            name="Benchmark",
            line=dict(color="rgb(16, 185, 129)"),
        )
    )
    cumReturnLineFig.add_trace(
        go.Scatter(
            x=results_df["Date"],
            y=results_df["cumulative_portfolio_strategy"],
            mode="lines",
            name="Strategy",
            line=dict(color="rgb(244, 63, 94)"),
        )
    )
    for stock, color in zip(
        ["AAPL", "AMZN", "GOOGL", "NFLX", "META"],
        ["#636EFA", "#AB63FA", "#19D3F3", "#FF6692", "#FF97FF", "#FECB52"],
    ):
        cumReturnLineFig.add_trace(
            go.Scatter(
                x=results_df["Date"],
                y=results_df[f"strategy_returns_{stock}"].cumsum(),
                mode="lines",
                name=f"{stock} Strategy",
                line=dict(color=color),  #! use px color
            )
        )
    cumReturnLineFig.update_layout(
        autosize=True,
        margin=dict(l=0, r=20, t=10, b=0),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="rgb(100,116,139)"),
        xaxis={"showticklabels": False, "title": "Date", "showgrid": False},
        yaxis={
            "title": "Cumulative Return",
            "showgrid": False,
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
    # daily std
    RollingStdFig = go.Figure()
    RollingStdFig.add_trace(
        go.Scatter(
            x=results_df["Date"],
            y=results_df["portfolio_returns"].rolling(21).std(),
            mode="lines",
            name="Benchmark",
            line=dict(color="rgb(16, 185, 129)"),
        )
    )
    RollingStdFig.add_trace(
        go.Scatter(
            x=results_df["Date"],
            y=results_df["portfolio_strategy"].rolling(21).std(),
            mode="lines",
            name="Strategy",
            line=dict(color="rgb(244, 63, 94)"),
        )
    )
    RollingStdFig.update_layout(
        autosize=True,
        margin=dict(l=0, r=20, t=10, b=0),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="rgb(100,116,139)"),
        xaxis={"showticklabels": False, "title": "Date", "showgrid": False},
        yaxis={
            "title": "Rolling Std",
            "showgrid": False,
            "zerolinecolor": "rgb(148, 163, 184)",
        },
        showlegend=False,
    )
    # distribution of daily strategy returns
    dailyReturnDistFig = px.histogram(
        results_df,
        x="portfolio_strategy",
        nbins=100,
        histnorm="probability",
    )
    dailyReturnDistFig.update_layout(
        autosize=True,
        margin=dict(l=0, r=20, t=10, b=0),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="rgb(100,116,139)"),
        xaxis={"showgrid": False, "title": "Daily Strategy Returns"},
        yaxis={"showgrid": False, "title": "Probability"},
    )
    return [
        html.Div(
            [
                html.Div(
                    [
                        # return
                        dcc.Graph(
                            figure=cumReturnLineFig,
                            config={"displayModeBar": False},
                            className="w-full h-full",
                        )
                    ],
                    className="h-[45%] w-full relative overflow-hidden zoomable shadow-lg hover:shadow-2xl rounded-lg bg-slate-800 transition duration-300 ease-in-out flex flex-col justify-center items-center p-1",
                ),
                html.Div(
                    [
                        # return
                        dcc.Graph(
                            figure=dailyReturnDistFig,
                            config={"displayModeBar": False},
                            className="w-full h-full",
                        )
                    ],
                    className="h-[45%] w-full relative overflow-hidden zoomable shadow-lg hover:shadow-2xl rounded-lg bg-slate-800 transition duration-300 ease-in-out flex flex-col justify-center items-center p-1",
                ),
            ],
            className="flex flex-col justify-evenly items-center p-0 h-full w-[45%] animate-fade-in animate-500",
        ),
        html.Div(
            [
                html.Div(
                    [
                        # return
                        dcc.Graph(
                            figure=drawDownFig,
                            config={"displayModeBar": False},
                            className="w-full h-full",
                        )
                    ],
                    className="h-[45%] w-full relative overflow-hidden zoomable shadow-lg hover:shadow-2xl rounded-lg bg-slate-800 transition duration-300 ease-in-out flex flex-col justify-center items-center p-1",
                ),
                html.Div(
                    [
                        # return
                        dcc.Graph(
                            figure=RollingStdFig,
                            config={"displayModeBar": False},
                            className="w-full h-full",
                        )
                    ],
                    className="h-[45%] w-full relative overflow-hidden zoomable shadow-lg hover:shadow-2xl rounded-lg bg-slate-800 transition duration-300 ease-in-out flex flex-col justify-center items-center p-1",
                ),
            ],
            className="flex flex-col justify-evenly items-center p-0 h-full w-[45%] animate-fade-in animate-500",
        ),
    ]


@callback(
    Output("analysis-page-visualisation-container", "children"),
    Input("analysis-page-visualisation-btn", "n_clicks"),
)
def showVisualisation(nClicks: int) -> list[html.Div]:
    if nClicks is None:
        raise PreventUpdate
    return visualisationComponentList()


def scrollAreaComponent():

    return html.Div(
        [
            html.Div(
                id="dummy-div-for-analysis-page-scroll-snap", style={"display": "none"}
            ),  # used for custom scroll snap speed
            html.Div(
                className="border-2 border-slate-600 h-dvh absolute top-0 left-[2rem] md:left-[5rem] translate-x-[-50%]",
            ),
            ################################
            # ending line
            html.Div(
                className="border-2 border-slate-900 h-[50%] absolute top-[650%] left-[2rem] md:left-[5rem] translate-x-[-50%]"
            ),
            html.Div(
                className="absolute rotate-45 -translate-x-1/2 -translate-y-1/2 bg-slate-900 top-[650%] left-[2rem] md:left-[5rem] w-[20px] h-[20px] md:w-8 md:h-8 self-end border-[4px] border-slate-600"
            ),
            ###########################################################
            #! This is the Title
            ###########################################################
            #! 1st dom
            timelineNode("Intro", "50%"),
            #! 2nd dom
            timelineNode("Impl", "150%"),
            #! 3rd dom
            timelineNode("Peek", "250%"),
            #! 4th dom
            timelineNode("Eval", "350%"),
            #! 5th dom
            timelineNode("Vis", "450%"),
            #! 6th dom
            timelineNode("Concl", "550%"),
            ###########################################################
            #! This is the scroll area
            ###########################################################
            #! 1st dom overview
            html.Div(
                [
                    html.Div(
                        [
                            html.H1(
                                "Strategy",
                                className="select-none text-xl lg:text-7xl font-semibold font-urbanist text-slate-50 px-3 py-1 z-50 antialiased",
                            ),
                            html.H1(
                                "Description",
                                className="select-none text-xl lg:text-7xl font-semibold font-urbanist text-slate-50 px-3 py-1 z-50 antialiased",
                            ),
                            html.P(
                                "Defining our approach, objectives, and expected outcomes.",
                                className="select-none w-[70vw] md:w-11/12 lg:w-5/6 text:sm lg:text-md font-semibold text-slate-400 px-4 py-1 z-50 mt-4",  #! px-4 to match the start with larger fonts
                            ),
                            html.Div(
                                html.Div(
                                    [
                                        html.H2(
                                            "Overview",
                                            className="text-slate-50 lg:text-xl",
                                        ),
                                        html.P(
                                            """
                                            - An integrated strategy that considers both trending and mean-reverting markets
                                        """,
                                            className="z-[2] text-slate-400 px-3 py-1 cursor-default hover:text-slate-300 transition duration-300 ease-in-out",
                                        ),
                                        html.P(
                                            """
                                            - A dynamic system that adjusts to overbought and oversold conditions
                                        """,
                                            className="z-[2] text-slate-400 px-3 py-1 cursor-default hover:text-slate-300 transition duration-300 ease-in-out",
                                        ),
                                        html.H2(
                                            "Objectives",
                                            className="text-slate-50 lg:text-xl",
                                        ),
                                        html.P(
                                            """
                                            - To outperform the market by capturing the persistence of trends
                                        """,
                                            className="z-[2] text-slate-400 px-3 py-1 cursor-default hover:text-slate-300 transition duration-300 ease-in-out",
                                        ),
                                        html.P(
                                            """
                                            - To minimize risk by identifying potential reversals and mean-reverting behavior
                                        """,
                                            className="z-[2] text-slate-400 px-3 py-1 cursor-default hover:text-slate-300 transition duration-300 ease-in-out",
                                        ),
                                        html.H2(
                                            "How It Works",
                                            className="text-slate-50 lg:text-xl",
                                        ),
                                        html.P(
                                            """
                                            - Utilize different indicators including Momentums, Hurst exponent, and RSI
                                        """,
                                            className="z-[2] text-slate-400 px-3 py-1 cursor-default hover:text-slate-300 transition duration-300 ease-in-out",
                                        ),
                                        html.P(
                                            """
                                            - Tune parameters to establish a rule-based method for signal generation
                                        """,
                                            className="z-[2] text-slate-400 px-3 py-1 cursor-default hover:text-slate-300 transition duration-300 ease-in-out",
                                        ),
                                        html.H2(
                                            "Expected Outcome",
                                            className="text-slate-50 lg:text-xl",
                                        ),
                                        html.P(
                                            """
                                            - Enhanced portfolio returns with controlled risk exposure
                                        """,
                                            className="z-[2] text-slate-400 px-3 py-1 cursor-default hover:text-slate-300 transition duration-300 ease-in-out",
                                        ),
                                        html.P(
                                            """
                                            - Robustness that withstands various market scenarios while generating alpha
                                        """,
                                            className="z-[2] text-slate-400 px-3 py-1 cursor-default hover:text-slate-300 transition duration-300 ease-in-out",
                                        ),
                                    ],
                                    className="relative overflow-auto w-auto h-auto rounded-lg  transition duration-300 ease-in-out lg:flex lg:flex-col justify-center items-start p-3",
                                ),
                                className="w-[calc(100dvw-10rem)] grow flex flex-row justify-start items-center p-0 ml-16 lg:ml-40 text-sm md:text-md lg:text-lg",
                            ),
                        ],
                        className="scroll-item-animate w-dvw h-dvh flex flex-col justify-start items-start p-4 ms-16 md:ms-40 overflow-hidden need-animate-600 need-animate-delay-200 need-animate-slide-in-x animate-slide-in-x animate-700 animate-delay-400",
                    ),
                ],
                #! this container need animation at first place because it is the first item
                className="scroll-item-container w-dvw h-dvh min-h-dvh flex flex-col justify-center items-start p-0 overflow-hidden snap-always snap-center transition duration-300 ease-in-out",
            ),
            #! 2nd dom logic
            html.Div(
                [
                    html.Div(
                        [
                            html.H1(
                                "Underlying",
                                className="select-none text-xl lg:text-7xl font-semibold font-urbanist text-slate-50 px-3 py-1 mt-1 z-50 antialiased",  #! mt-1 to match the top with 'data' kind of low height characters
                            ),
                            html.H1(
                                "Methodology",
                                className="select-none text-xl lg:text-7xl font-semibold font-urbanist text-slate-50 px-3 py-1 z-50 antialiased",
                            ),
                            html.P(
                                "Explaining the logic, mechanisms, and techniques used in the strategy.",
                                className="select-none w-[70vw] md:w-11/12 lg:w-5/6 text:sm lg:text-md font-semibold text-slate-400 px-4 py-1 z-50 mt-4",
                            ),
                            html.Div(
                                html.Div(
                                    [
                                        html.H2(
                                            "Foundations",
                                            className="text-slate-50 lg:text-xl",
                                        ),
                                        dcc.Markdown(
                                            """
                                            \- Based on a weak form of the **market efficiency** hypothesis, which states that past price information is already reflected in current prices
                                        """,
                                            className="z-[2] text-slate-400 px-3 py-1 cursor-default hover:text-slate-300 transition duration-300 ease-in-out",
                                        ),
                                        dcc.Markdown(
                                            """
                                            \- Assume stocks can exhibit **persistent trends** and markets can **revert to the mean** to improve adaptability and robustness
                                        """,
                                            className="z-[2] text-slate-400 px-3 py-1 cursor-default hover:text-slate-300 transition duration-300 ease-in-out",
                                        ),
                                        html.H2(
                                            "Indicators",
                                            className="text-slate-50 lg:text-xl",
                                        ),
                                        dcc.Markdown(
                                            """
                                            \- **Momentum** \[window=5,21\] provides a snapshot of ongoing trends
                                        """,
                                            className="z-[2] text-slate-400 px-3 py-1 cursor-default hover:text-slate-300 transition duration-300 ease-in-out",
                                        ),
                                        dcc.Markdown(
                                            """
                                            \- **Hurst Exponent** \[window=200, threshold=0.5\] validates whether the observed momentum is part of a larger persistent trend or a short-lived fluctuation
                                        """,
                                            className="z-[2] text-slate-400 px-3 py-1 cursor-default hover:text-slate-300 transition duration-300 ease-in-out",
                                        ),
                                        dcc.Markdown(
                                            """
                                            \- **RSI** \[threshold=30,70\] gauges the market's emotional extremes, marking potential overbought or oversold conditions
                                        """,
                                            className="z-[2] text-slate-400 px-3 py-1 cursor-default hover:text-slate-300 transition duration-300 ease-in-out",
                                        ),
                                        html.H2(
                                            "Strategy Mechanism",
                                            className="text-slate-50 lg:text-xl",
                                        ),
                                        dcc.Markdown(
                                            """
                                            \- **Decision making** utilises momentum and Hurst exponent for primary triggers, and RSI providing additional context for entries and exits
                                        """,
                                            className="z-[2] text-slate-400 px-3 py-1 cursor-default hover:text-slate-300 transition duration-300 ease-in-out",
                                        ),
                                        dcc.Markdown(
                                            """
                                            \- **Signal generation** follows the rules derived from above parameters to signal buy, sell, or hold actions
                                        """,
                                            className="z-[2] text-slate-400 px-3 py-1 cursor-default hover:text-slate-300 transition duration-300 ease-in-out",
                                        ),
                                    ],
                                    className="relative overflow-auto w-auto max-w-[85%] lg:max-w-[75%] h-auto rounded-lg  transition duration-300 ease-in-out lg:flex lg:flex-col justify-center items-start p-3",
                                ),
                                className="w-[calc(100dvw-10rem)] grow flex flex-row justify-start items-center p-0 ml-16 lg:ml-40 text-sm md:text-md lg:text-lg",
                            ),
                        ],
                        className="scroll-item-animate w-dvw h-dvh flex flex-col justify-start items-start p-4 ms-16 md:ms-40 overflow-hidden need-animate-600 need-animate-delay-200 need-animate-slide-in-x",  # animate-slide-in-x animate-700 animate-delay-400
                    ),
                ],
                className="scroll-item-container w-dvw h-dvh min-h-dvh flex flex-col justify-center items-start p-0 overflow-hidden snap-always snap-center transition duration-300 ease-in-out opacity-0",  #! opacity-0 to hide the dom > 1st
            ),
            #! 3rd dom full trade table
            html.Div(
                [
                    html.Div(
                        [
                            html.H1(
                                "Signal",
                                className="select-none text-xl lg:text-7xl font-semibold font-urbanist text-slate-50 px-3 py-1 z-50 antialiased",
                            ),
                            html.H1(
                                "Generation",
                                className="select-none text-xl lg:text-7xl font-semibold font-urbanist text-slate-50 px-3 py-1 z-50 antialiased",
                            ),
                            html.P(
                                "Taking a closer look at the data frame generated from the strategy's output based on MAANG stocks.",
                                className="select-none w-[70vw] md:w-11/12 lg:w-5/6 text:sm lg:text-md font-semibold text-slate-400 px-4 py-1 z-50 mt-4",
                            ),
                            html.Div(
                                html.Div(
                                    [
                                        # html.Div(className="h-full w-full absolute bg-slate-700 animate-pulse z-[1]"),
                                        dcc.Markdown(
                                            """
                                            ```python
                                            
                                            # Hurst exponent greater than 0.5, short term and long term momentum greater than 0, buy
                                            data.loc[(data['Hurst'] > 0.5) & (data['ShortTermMomentum'] > 0) & (data['LongTermMomentum'] > 0), 'Position'] = 1
                                            data.loc[(data['Hurst'] > 0.5) & (data['ShortTermMomentum'] < 0) & (data['LongTermMomentum'] < 0), 'Position'] = -1
                                            # Out of the market
                                            data.loc[(data['RSI'] <= 70) & (data['Hurst'] > 0.5) & ((data['ShortTermMomentum'] > 0) & (data['LongTermMomentum'] < 0) | (data['ShortTermMomentum'] < 0) & (data['LongTermMomentum'] > 0)), 'Position'] = 1
                                            data.loc[(data['RSI'] > 70) & (data['Hurst'] > 0.5) & ((data['ShortTermMomentum'] > 0) & (data['LongTermMomentum'] < 0) | (data['ShortTermMomentum'] < 0) & (data['LongTermMomentum'] > 0)), 'Position'] = -1
                                            data.loc[(data['Hurst'] < 0.5) & (data['RSI'] <= 70), 'Position'] = 1
                                            data.loc[(data['Hurst'] < 0.5) & (data['RSI'] > 70), 'Position'] = -1
                                            
                                            ```
                                            """,
                                            className="z-[2] blur-sm",
                                        ),
                                        html.Button(
                                            ">> View Result <<",
                                            id="analysis-page-infinite-grid-full-trades-btn",
                                            className="z-[3] text-md font-semibold text-slate-400 px-3 py-1 cursor-default transition duration-300 ease-in-out rounded-lg animate-pulse absolute left-1/2 -translate-x-1/2",
                                        ),
                                    ],
                                    id="analysis-page-infinite-grid-full-trades-container",
                                    className="relative overflow-hidden zoomable w-3/4 h-3/4 shadow-lg hover:shadow-2xl rounded-lg bg-slate-800 transition duration-300 ease-in-out flex flex-col justify-center items-center p-1",
                                ),
                                className="w-[calc(100dvw-10rem)] grow flex flex-row justify-center items-center p-0",
                            ),
                        ],
                        className="scroll-item-animate w-dvw h-dvh flex flex-col justify-start items-start p-4 ms-16 md:ms-40 overflow-hidden need-animate-600 need-animate-delay-200 need-animate-slide-in-x",  # animate-slide-in-x animate-700 animate-delay-400
                    ),
                ],
                className="scroll-item-container w-dvw h-dvh min-h-dvh flex flex-col justify-center items-start p-0 overflow-hidden snap-always snap-center transition duration-300 ease-in-out opacity-0",  #! opacity-0 to hide the dom > 1st
            ),
            #! 4th dom metrics
            html.Div(
                [
                    html.Div(
                        className="border-2 border-slate-200 h-dvh fixed top-0 left-[2rem] md:left-[5rem] translate-x-[-50%]",
                    ),
                    html.Div(
                        [
                            html.H1(
                                "Strategy",
                                className="select-none text-xl lg:text-7xl font-semibold font-urbanist text-slate-50 px-3 py-1 z-50 antialiased",
                            ),
                            html.H1(
                                "Evaluation",
                                className="select-none text-xl lg:text-7xl font-semibold font-urbanist text-slate-50 px-3 py-1 z-50 antialiased",
                            ),
                            html.P(
                                "Measuring the performance of our strategy against the market benchmark using different metrics.",
                                className="select-none w-[70vw] md:w-11/12 lg:w-5/6 text:sm lg:text-md font-semibold text-slate-400 px-4 py-1 z-50 mt-4",
                            ),
                            html.Div(
                                html.Div(
                                    [
                                        # html.Div(className="h-full w-full absolute bg-slate-700 animate-pulse z-[1]"),
                                        html.P(
                                            """
                                            We evaluate the performance of our strategy by comparing it to the market benchmark, i.e., buy & hold strategy for MAANG. The metrics mainly include standard deviation, annualised return, and Sharpe ratio. Overall, our strategy is showing promising results with a higher return and lower risk compared to the benchmark.
                                            """,
                                            className="z-[2] text-slate-500 hover:text-slate-400 px-3 py-1 cursor-default transition duration-300 ease-in-out",
                                        ),
                                        html.Button(
                                            ">> View Result <<",
                                            id="analysis-page-infinite-grid-metrics-btn",
                                            className="z-[3] text-md font-semibold text-slate-400 px-3 py-1 cursor-default transition duration-300 ease-in-out rounded-lg animate-pulse",
                                        ),
                                    ],
                                    id="analysis-page-infinite-grid-metrics-container",
                                    className="relative overflow-hidden zoomable w-3/4 h-3/4 shadow-lg hover:shadow-2xl rounded-lg bg-slate-800 transition duration-300 ease-in-out flex flex-col justify-center items-center p-1",
                                ),
                                className="w-[calc(100dvw-10rem)] grow flex flex-row justify-center items-center p-0",
                            ),
                        ],
                        className="scroll-item-animate w-dvw h-dvh flex flex-col justify-start items-start p-4 ms-16 md:ms-40 overflow-hidden need-animate-600 need-animate-delay-200 need-animate-slide-in-x",  # animate-slide-in-x animate-700 animate-delay-400
                    ),
                ],
                className="scroll-item-container w-dvw h-dvh min-h-dvh flex flex-col justify-center items-start p-0 overflow-hidden snap-always snap-center transition duration-300 ease-in-out opacity-0",  #! opacity-0 to hide the dom > 1st
            ),
            #! 5th dom charting
            html.Div(
                [
                    html.Div(
                        className="border-2 border-slate-200 h-dvh fixed top-0 left-[2rem] md:left-[5rem] translate-x-[-50%]",
                    ),
                    html.Div(
                        [
                            html.H1(
                                "Result",
                                className="select-none text-xl lg:text-7xl font-semibold font-urbanist text-slate-50 px-3 py-1 z-50 antialiased",
                            ),
                            html.H1(
                                "Visualisation",
                                className="select-none text-xl lg:text-7xl font-semibold font-urbanist text-slate-50 px-3 py-1 z-50 antialiased",
                            ),
                            html.P(
                                "Visualising the performance of our strategy using different charts besides the ones presented in the dashboard.",
                                className="select-none w-[70vw] md:w-11/12 lg:w-5/6 text:sm lg:text-md font-semibold text-slate-400 px-4 py-1 z-50 mt-4",
                            ),
                            html.Div(
                                [
                                    html.Div(
                                        [
                                            html.Button(
                                                ">> Visualise Now <<",
                                                id="analysis-page-visualisation-btn",
                                                className="z-[3] text-md lg:text-xl font-semibold text-slate-400 px-3 py-1 cursor-default transition duration-300 ease-in-out rounded-lg",
                                            )
                                        ],
                                        className="w-[90%] h-[90%] bg-slate-800 flex flex-col justify-center items-center p-1 rounded-lg shadow-lg hover:shadow-2xl animate-pulse",
                                    )
                                ],
                                id="analysis-page-visualisation-container",
                                className="w-[calc(100dvw-10rem)] h-3/4 flex max-h-[75%] flex-row justify-center items-center gap-4 p-0",
                            ),
                        ],
                        className="scroll-item-animate w-dvw h-dvh flex flex-col justify-start items-start p-4 ms-16 md:ms-40 overflow-hidden need-animate-600 need-animate-delay-200 need-animate-slide-in-x",  # animate-slide-in-x animate-700 animate-delay-400
                    ),
                ],
                className="scroll-item-container w-dvw h-dvh min-h-dvh flex flex-col justify-center items-start p-0 overflow-hidden snap-always snap-center transition duration-300 ease-in-out opacity-0",  #! opacity-0 to hide the dom > 1st
            ),
            #! 6th dom challenges & opportunities
            html.Div(
                [
                    html.Div(
                        className="border-2 border-slate-200 h-dvh fixed top-0 left-[2rem] md:left-[5rem] translate-x-[-50%]",
                    ),
                    html.Div(
                        [
                            html.H1(
                                "Challenges &",
                                className="select-none text-xl lg:text-7xl font-semibold font-urbanist text-slate-50 px-3 py-1 z-50 antialiased",
                            ),
                            html.H1(
                                "Opportunities",
                                className="select-none text-xl lg:text-7xl font-semibold font-urbanist text-slate-50 px-3 py-1 z-50 antialiased",
                            ),
                            html.P(
                                "Discussing the potential downsides and future vision of our strategy.",
                                className="select-none w-[70vw] md:w-11/12 lg:w-5/6 text:sm lg:text-md font-semibold text-slate-400 px-4 py-1 z-50 mt-4",
                            ),
                            html.Div(
                                html.Div(
                                    [
                                        html.H2(
                                            "Challenges",
                                            className="text-slate-50 lg:text-xl",
                                        ),
                                        dcc.Markdown(
                                            """
                                            \- **Market noise** exists in the form of random fluctuations that can mislead the strategy's decision-making process
                                        """,
                                            className="z-[2] text-slate-400 px-3 py-1 cursor-default hover:text-slate-300 transition duration-300 ease-in-out",
                                        ),
                                        dcc.Markdown(
                                            """
                                            \- **Indicator lagging** delays response to market changes which may lead to missed opportunities or false signals
                                        """,
                                            className="z-[2] text-slate-400 px-3 py-1 cursor-default hover:text-slate-300 transition duration-300 ease-in-out",
                                        ),
                                        dcc.Markdown(
                                            """
                                            \- **Complexity** raised by multiple indicators and parameters leads to a bias-variance trade-off
                                        """,
                                            className="z-[2] text-slate-400 px-3 py-1 cursor-default hover:text-slate-300 transition duration-300 ease-in-out",
                                        ),
                                        html.H2(
                                            "Opportunities",
                                            className="text-slate-50 lg:text-xl",
                                        ),
                                        dcc.Markdown(
                                            """
                                            \- **Diversified strategy** reduces reliance on a single indicator
                                        """,
                                            className="z-[2] text-slate-400 px-3 py-1 cursor-default hover:text-slate-300 transition duration-300 ease-in-out",
                                        ),
                                        dcc.Markdown(
                                            """
                                            \- **Extensible framework** allows for future improvements and adaptability to new market conditions
                                        """,
                                            className="z-[2] text-slate-400 px-3 py-1 cursor-default hover:text-slate-300 transition duration-300 ease-in-out",
                                        ),
                                        dcc.Markdown(
                                            """
                                            \- **Parameter tuning** can be optimised for more recent datasets to enhance the strategy's performance and robustness
                                        """,
                                            className="z-[2] text-slate-400 px-3 py-1 cursor-default hover:text-slate-300 transition duration-300 ease-in-out",
                                        ),
                                    ],
                                    id="analysis-page-challenges-and-opportunities-container",
                                    className="relative overflow-auto w-auto max-w-[85%] lg:max-w-[75%] h-auto rounded-lg -translate-y-[10%] lg:flex lg:flex-col justify-center items-start p-3",
                                ),
                                className="w-[calc(100dvw-10rem)] grow flex flex-row justify-start items-center p-0 ml-16 lg:ml-40 text-sm md:text-md lg:text-lg",
                            ),
                        ],
                        className="scroll-item-animate w-dvw h-dvh flex flex-col justify-start items-start p-4 ms-16 md:ms-40 overflow-hidden need-animate-600 need-animate-delay-200 need-animate-slide-in-x",  # animate-slide-in-x animate-700 animate-delay-400
                    ),
                ],
                className="scroll-item-container w-dvw h-dvh min-h-dvh flex flex-col justify-center items-start p-0 overflow-hidden snap-always snap-center transition duration-300 ease-in-out opacity-0",  #! opacity-0 to hide the dom > 1st
            ),
            #! 7th dom challenges & opportunities
            html.Div(
                [
                    html.Div(
                        className="border-2 border-slate-200 h-dvh fixed top-0 left-[2rem] md:left-[5rem] translate-x-[-50%]",
                    ),
                    html.Div(
                        [
                            html.H1(
                                "Thank You.",
                                className="scroll-item-animate need-animate-600 need-animate-delay-200 need-animate-slide-in-x select-none sm:text-xl md:text-4xl lg:text-7xl font-normal font-urbanist text-slate-300 px-3 py-1 z-50 antialiased",
                            ),
                            html.P(
                                "Liu Chang",
                                className="absolute right-2 top-[675%] scroll-item-animate need-animate-600 need-animate-delay-800 need-animate-slide-in-x select-none sm:text-sm md:text-md lg:text-xl font-normal font-urbanist text-slate-400 px-3 py-1 z-50 antialiased",
                            ),
                            html.P(
                                "Geng Yihan",
                                className="absolute right-2 top-[680%] scroll-item-animate need-animate-600 need-animate-delay-1000 need-animate-slide-in-x select-none sm:text-sm md:text-md lg:text-xl font-normal font-urbanist text-slate-400 px-3 py-1 z-50 antialiased",
                            ),
                            html.P(
                                "Huang Yunqi",
                                className="absolute right-2 top-[685%] scroll-item-animate need-animate-600 need-animate-delay-1200 need-animate-slide-in-x select-none sm:text-sm md:text-md lg:text-xl font-normal font-urbanist text-slate-400 px-3 py-1 z-50 antialiased",
                            ),
                            html.P(
                                "Xu Fengyuan",
                                className="absolute right-2 top-[690%] scroll-item-animate need-animate-600 need-animate-delay-1400 need-animate-slide-in-x select-none sm:text-sm md:text-md lg:text-xl font-normal font-urbanist text-slate-400 px-3 py-1 z-50 antialiased",
                            ),
                            html.P(
                                "Nicholas, Lian Jie",
                                className="absolute right-2 top-[695%] scroll-item-animate need-animate-600 need-animate-delay-1600 need-animate-slide-in-x select-none sm:text-sm md:text-md lg:text-xl font-normal font-urbanist text-slate-400 px-3 py-1 z-50 antialiased",
                            ),
                            ],
                        className="w-dvw h-dvh flex flex-col justify-center items-start p-4 ms-16 md:ms-40 overflow-hidden ",  # animate-slide-in-x animate-700 animate-delay-400
                    ),
                ],
                className="scroll-item-container w-dvw h-dvh min-h-dvh flex flex-col justify-center items-start p-0 overflow-hidden snap-always snap-center transition duration-300 ease-in-out opacity-0",  #! opacity-0 to hide the dom > 1st
            ),
        
        
        ],
        id="analysis-page-scroll-container",
        className="scroll-container w-dvw h-dvh flex flex-col justify-start items-start overflow-y-auto overflow-x-hidden scroll-smooth animate-slide-in-y animate-700 snap-y snap-mandatory box-content pr-[17px]",  #! to hide the scrollbar
    )


def paperWrapperComponent(dom):
    return html.Div(
        [dom],
        className="w-full h-full flex flex-col justify-center items-center p-0 bg-slate-800 rounded-lg shadow-lg hover:shadow-2xl",
    )


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
                                            "Demo ▶️",
                                            id="demo-btn",
                                            className="w-full h-10 bg-slate-700 text-slate-200 text-xs md:text-sm lg:text-md font-semibold rounded-md hover:bg-slate-600 focus:bg-slate-600 transition duration-300 ease-in-out",
                                        )
                                    ],
                                    className="absolute bottom-2 right-4 w-[30%] h-[20%] hidden",
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


def bar():
    dec.DashECharts(
        option={
            "xAxis": {
                "type": "category",
                # rolling 200 days
                "data": results_df["Date"].iloc[::200].to_list(),
            },
            "yAxis": {"type": "value"},
            "tooltip": {},
            "series": [
                {
                    "data": results_df["cumulative_portfolio_returns"]
                    .iloc[::200]
                    .to_list(),
                    "type": "bar",
                    "smooth": True,
                },
                {
                    "data": results_df["cumulative_portfolio_strategy"]
                    .iloc[::200]
                    .to_list(),
                    "type": "bar",
                    "smooth": True,
                },
            ],
        },
        style={
            "width": "25dvw",
            "height": "33dvh",
        },
    )


def analysisPage():
    return html.Div(
        [
            html.Div(
                #! Strange bug, the translate-x-[-50%] is not working. Using style as workaround
                style={"translate": "-50%"},
                className="border-2 border-slate-600 h-dvh absolute top-0 left-[2rem] md:left-[5rem] animate-slide-in-y animate-700 animate-delay-1400",
            ),
            dcc.Interval(
                id="analysis-page-title-interval",
                interval=2500,
                max_intervals=1,
                n_intervals=0,
            ),
            html.Div(
                [
                    html.Div(
                        [
                            html.H1(
                                "Data",
                                className="select-none text-3xl lg:text-9xl font-semibold font-urbanist text-slate-50 px-3 py-1 z-50 antialiased",
                            ),
                            html.H1(
                                "Analysis",
                                className="select-none text-3xl lg:text-9xl font-semibold font-urbanist text-slate-50 px-3 py-1 z-50 antialiased",
                            ),
                            html.P(
                                "...Unleash the potential of Momentum, RSI, and more.",
                                className="translate-x-[20%] select-none w-[70vw] md:w-11/12 lg:w-5/6 text:sm lg:text-md font-semibold text-slate-400 px-3 py-1 z-50 mt-4",
                            ),
                        ],
                        className="w-dvw h-dvh flex flex-col justify-center items-start p-4 ms-8 overflow-hidden animate-slide-in-x-and-out-y animate-2500 animate-delay-400",
                    ),
                ],
                id="analysis-page-inner-container",
                className="w-dvw h-dvh flex flex-col justify-center items-start p-0 overflow-hidden",
            ),
        ],
        id="analysis-page-container",
        className="w-dvw h-dvh flex flex-col justify-center p-0 overflow-hidden",
    )


def landingPage() -> html.Div:
    """Landing page layout.

    Returns:
        html.Div: landing page layout.
    """
    bufferSymbol = "EUR_USD"
    candlestickData = fetch_data(bufferSymbol, 200)
    logger.info(
        f"Landing page layout. yfinance data downloaded for {bufferSymbol}. len: {len(candlestickData)}"
    )
    return html.Div(
        [
            # dcc.Store(
            #     id="landing-page-candlestick-chart-store",
            #     data={bufferSymbol: bufferData},
            #     storage_type="memory",
            # ),
            # navbar
            html.Nav(
                [
                    html.Button(
                        ["- EUR/USD -"],
                        className="text-md font-semibold text-slate-400 px-3 py-1 cursor-default hover:bg-slate-800 transition duration-300 ease-in-out rounded-lg focus:ring focus:ring-slate-800 focus:ring-opacity-50 focus:bg-slate-800",
                    ),
                    # floating right
                    html.Div(
                        ["💴Version FX💵"],
                        className="absolute right-2 text-lg font-semibold text-slate-300 hover:text-slate-200 select-none px-3 py-1 cursor-default transition duration-300 ease-in-out",
                    )
                ],
                className="fixed top-0 w-dvw h-16 bg-slate-900 flex flex-row gap-1 justify-center items-center p-1 z-50",
            ),
            html.Div(
                [
                    html.Div(
                        [
                            html.H1(
                                "Visualise",
                                className="select-none text-3xl lg:text-7xl font-semibold font-urbanist text-slate-50 px-3 py-1 z-50 antialiased",
                            ),
                            html.H3(
                                "Our Trading Strategies",
                                className="select-none text-nowrap text-lg lg:text-4xl font-semibold font-urbanist text-indigo-300 px-3 pb-1 z-50 antialiased underline decoration-indigo-300 decoration-solid decoration-2",
                            ),
                            html.P(
                                "Trading FX in real-time with Oanda API. This work is based on the project of the course FT5010 Algorithmic Trading Systems Design and Deployment.",
                                className="select-none w-[70vw] md:w-11/12 lg:w-5/6 text:sm lg:text-md font-semibold text-slate-400 px-3 py-1 z-50 mt-4",
                            ),
                            html.Button(
                                ">> EXPLORE NOW",
                                id="landing-page-explore-now-btn",
                                className="select-none text-md font-semibold text-slate-50 px-3 py-1 z-50 mt-4 animate-pulse",
                            ),
                        ],
                        className="h-1/2 w-full flex flex-col justify-start items-start p-4 mb-4 z-[999]",
                    ),
                    html.Div(className="z-[99] absolute w-1/2 h-full -ml-4 bg-slate-800 opacity-[95%] z-[99] rounded-r-full shadow-lg shadow-slate-950")
                ],
                className="w-1/2 h-full flex flex-col justify-center items-start p-4 bg-slate-900 mb-4",
            ),
            html.Div(
                [
                    html.Div(
                        [
                            dash_tvlwc.Tvlwc(
                                id="landing-page-candlestick-chart",
                                seriesData=[candlestickData],
                                seriesTypes=["candlestick"],
                                seriesOptions=[
                                    {
                                        "priceLineVisible": False,
                                        "LineSeriesOptions": {"lastPriceAnimation": 1},
                                    }
                                ],
                                chartOptions={
                                    "layout": {
                                        "background": {
                                            "type": "solid",
                                            "color": "rgb(15 23 42)",
                                        },
                                        "textColor": "rgb(203 213 225)",
                                        "fontFamily": "Urbanist",
                                    },
                                    "grid": {
                                        "vertLines": {"visible": False},
                                        "horzLines": {"visible": False},
                                    },
                                    # "handleScroll": {"mouseWheel": False, "pressedMouseMove": False},
                                    "leftPriceScale": {
                                        "borderVisible": False,
                                        "visible": False,
                                    },
                                    "rightPriceScale": {
                                        "borderVisible": False,
                                        "visible": False,
                                    },
                                    "timeScale": {
                                        # "lockVisibleTimeRangeOnResize":True,
                                        "borderVisible": False,
                                        "timeVisible": True,
                                        "secondsVisible": True,
                                        # "visible": False,
                                        "fixLeftEdge": True,
                                        # "fixRightEdge": True, #! this is causing value null error as data dynamically pushed
                                        # "lockVisibleTimeRange": True,
                                    },
                                    "crosshair": {
                                        "horzLine": {"labelVisible": False},
                                        "vertLine": {"labelVisible": False},
                                    },
                                },
                                width="100dvw",
                                height="100dvh",
                            ),
                            dcc.Interval(
                                id="landing-page-candlestick-chart-interval",
                                interval=5 * 1000,  # in milliseconds
                                n_intervals=0,
                            ),
                        ],
                        className="w-dvw h-dvh fixed right-0 z-0",
                    )
                ],
                className="w-1/2 h-dvh flex flex-col justify-center items-start p-0 bg-slate-900",
            ),
        ],
        id="landing-page-container",
        className="w-dvw h-dvh flex flex-row justify-center items-start p-0 overflow-hidden",
    )


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


@callback(
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


@callback(
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


@callback(
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
        return analysisPage()
    logger.info(f"Switch to landing page for {pathname}.")
    return landingPage()


if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0")
