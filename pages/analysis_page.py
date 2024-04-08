from dash import html, dcc
from components.common.wrappers import timelineNode
def analysisDetailPage():

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

def analysisInitialPage():
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
