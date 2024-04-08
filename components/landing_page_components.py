from dash import html, dcc
from dash_tvlwc import Tvlwc
from services.strategy_utils import fetch_data
from configs.server_conf import logger
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
                    # html.Button(
                    #     ["- EUR/USD -"],
                    #     className="text-md font-semibold text-slate-400 px-3 py-1 cursor-default hover:bg-slate-800 transition duration-300 ease-in-out rounded-lg focus:ring focus:ring-slate-800 focus:ring-opacity-50 focus:bg-slate-800",
                    # ),
                    # floating right
                    html.Div(
                        ["Version @FX"],
                        className="absolute right-2 text-md font-semibold text-slate-400 hover:text-slate-200 select-none px-3 py-1 cursor-default transition duration-300 ease-in-out",
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
                            Tvlwc(
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
